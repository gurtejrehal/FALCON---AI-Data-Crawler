from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Keyword, Category, Link, CrawledLinks
from scheduler.models import ScrapedLink
from django.contrib import messages
from utils.crawler_spider import crawling, count_items, wiki_data, wiki_scraping, social_media_scrape, extract_image
from utils.news import news
from utils.analytics import category_percent, category_count, keyword_trends
import random, copy, json
from django.http import JsonResponse
from django.db.models import Count


@login_required
def index(request):
    """

    :param request:
    :return: Home Page
    """
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    category = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')

    unread = notifications.filter(read=False)

    user_crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by('-pub_date')

    context = dict()
    context['home'] = True
    context['category'] = category
    context['userprofile'] = userprofile
    context['notifications'] = notifications[:5]
    context['unread_count'] = len(unread)
    context['user_crawler'] = user_crawled_links[:5]
    context['cat_percent'] = category_percent(request.user)

    return render(request, "crawler/index.html", context=context)




@login_required
def crawler_index(request):
    """

    :param request:
    :return: Crawler Page
    """
    context = dict()
    userprofile = UserProfile.objects.get(user=request.user)
    notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')
    unread = notifications.filter(read=False)
    categories = [i.name for i in Category.objects.all()]
    crawled_links = CrawledLinks.objects.order_by('-pub_date')

    unique_keyword = list(crawled_links.filter(userprofile=userprofile).order_by().values_list('link__keyword__name', flat=True).distinct())

    copy_keyword = copy.copy(unique_keyword)
    random.shuffle(copy_keyword)

    keywords_labels, keywords_dataset = keyword_trends(copy_keyword[1:6])

    print(category_count(request.user))
    context['crawler_home'] = True
    context['userprofile'] = userprofile
    context['notifications'] = notifications[:5]
    context['unread_count'] = len(unread)
    context['crawled_links'] = crawled_links
    context['categories'] = categories
    context['category_data'] = category_count(request.user)
    context['unique_keyword'] = unique_keyword
    context['keywords_labels'] = keywords_labels
    context['keywords_dataset'] = keywords_dataset

    return render(request, "crawler/crawler.html", context=context)


@login_required
def report(request):
    """

    :param request:
    :return: Detailed Report
    """
    context = dict()
    render_dict = dict()
    temp = dict()
    category = Category.objects.all()
    userprofile = UserProfile.objects.get(user=request.user)
    notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')

    unread = notifications.filter(read=False)

    crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by('pub_date')
    categories = [i.name for i in Category.objects.all()]
    unique_keywords = list(crawled_links.values_list('link__keyword__name', flat=True).distinct())

    for keyword in unique_keywords:
        for category in categories:
            temp[category] = CrawledLinks.objects.filter(userprofile=userprofile, link__keyword__name=keyword, link__category__name=category)
        context[keyword] = temp

    print(context)
    render_dict['report'] = True
    render_dict['category'] = category
    render_dict['userprofile'] = userprofile
    render_dict['notifications'] = notifications[:5]
    render_dict['unread_count'] = len(unread)
    render_dict['data'] = context
    return render(request, "crawler/report.html", context=render_dict)
    # return HttpResponse(context)

@login_required
def test(request):
    """

    :param request:
    :return: Beta Testing
    """
    userprofile = UserProfile.objects.get(user=request.user)
    context = dict()
    context['userprofile'] = userprofile
    return render(request, "crawler/result.html", context=context)


@login_required
def social(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        scrape_data = social_media_scrape(keyword)
        context = {
            'scrape_data': scrape_data
        }
        return render(None, 'crawler/social.html', context=context)


@login_required
def update(request):
    """

    :param request:
    :return: update profile settings
    """
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        query = str(request.POST['query'])
        userprofile.concurrency = int(query)
        update_percent = (userprofile.concurrency / 10) * 100
        userprofile.save()

        content = "Concurrency updated successfully."
        notification = Notifications(user=userprofile, content=content)
        notification.save()

        messages.success(request, content, extra_tags='concurrent_update')
        new_notification = Notifications.objects.filter(user=userprofile, read=False)

        context = {
            'update': query,
            'update_percent': update_percent,
            'new_count': len(new_notification)
        }

        return render(request, 'crawler/update.html', context=context)


@login_required
def update_notifications(request):
    """

    :param request:
    :return: generate report Notifications
    """
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        keyword = str(request.POST['keyword'])
        content = f"Report is being generated for '{keyword}'"
        notification = Notifications(user=userprofile, content=content)
        notification.save()

        return HttpResponse("1")


@login_required
def update_notifications_base(request):
    """

    :param request:
    :return: Notifications
    """
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')

        context = {
            'notifications': notifications[:5]
        }

        return render(None, "crawler/update_notifications.html", context=context)


@login_required
def read(request):
    """

    :param request:
    :return: Notifcations read/unread
    """
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile)

        for notification in notifications:
            notification.read = True
            notification.save()

        return HttpResponse("0")


def api(request, keyword):
    """

    :param request:
    :param keyword:
    :return: Falcon Custom API
    """
    temp = dict()
    result = news(keyword)
    userprofile = UserProfile.objects.get(user=request.user)
    key = Keyword.objects.get(name=keyword)
    crawled_links = CrawledLinks.objects.filter(userprofile=userprofile, link__keyword=key)

    for link in crawled_links:
        temp[link.link.link] = link.link.scrape_data

    temp["summarized data"] = result
    data = {
        keyword: temp
    }
    return JsonResponse(data)


@login_required
def process(request):
    """

    :param request:
    :return: Result Page
    """
    if request.method == 'POST':

        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')
        unread = notifications.filter(read=False)

        main_search = request.POST.get('main_search')
        filters = request.POST['multiple_select']
        reschedule_crawler = request.POST.get('reschedule_crawler')
        print(type(main_search), type(filters))

        main_search_list = [x.strip(' ') for x in main_search.split(',')]
        filters_list = [x.strip(' ') for x in filters.split(',')]

        result1 = dict()
        result2 = dict()
        result3 = dict()
        result4 = dict()
        news_data1 = dict()
        news_data2 = dict()
        list1 = list()
        list2 = list()
        temp_list1 = list()
        wiki_links = list()
        video_links = list()
        pdfs = list()
        images = list()
        scrape_data = ""
        no_of_links = 0
        no_of_scrape = 0
        wiki_scrape_temp = dict()
        scrape_data_dict = dict()
        scrape_data_dict_main = dict()
        colors = ['#111', '#f59042', '#555644', '#444']

        # print(result1)

        print(filters_list)

        for keyword in main_search_list:
            query = Keyword.objects.get_or_create(name=keyword)[0]
            query.save()
            pipeline_result = crawling(keyword, filters_list)[2]
            # pipeline_scraper_result = crawling(keyword, filters_list)[3]

            for category, links in zip(filters_list, pipeline_result):

                cat = Category.objects.get_or_create(name=category)[0]

                for link in links:
                    print(link[0])
                    # print(link[1])
                    if "wikipedia" in link[0]:
                        scrape_data, empty = wiki_scraping(link[0])
                        no_of_scrape += 1
                        wiki_links.append(link[0])
                        if not empty:
                            wiki_scrape_temp[str(link[0])] = scrape_data

                    elif link[0].endswith("pdf"):
                        pdfs.append(link[0])

                    elif "youtube" in link[0]:
                        video_links.append(link[0])

                    else:
                        scrape_data = link[1]
                        images.append(extract_image(scrape_data))

                    scrape_data_dict[link[0]] = scrape_data

                    scraped_link = ScrapedLink.objects.get_or_create(link=link[0], scrape_data=scrape_data,
                                                                     schedule_day=reschedule_crawler)[0]
                    scraped_link.save()

                    link = Link.objects.get_or_create(keyword=query, category=cat, link=link[0], scrape_data=scrape_data)[0]
                    link.save()

                    profile_update, created = CrawledLinks.objects.get_or_create(userprofile=userprofile,
                                                                                 link=link, reschedule=reschedule_crawler)
                    profile_update.save()

                    if created:
                        no_of_links += 1

            scrape_data_dict_main[keyword] = scrape_data_dict

        userprofile.crawled_links += no_of_links
        userprofile.scraped_data += no_of_scrape
        userprofile.save()

        if len(main_search_list) > 2:
            list1 = main_search_list[:2]
            list2 = main_search_list[2:]

        else:
            list1 = main_search_list

        for query in list1:
            result1[query] = crawling(query, filters_list)[0]
            # result2[query] = crawling(query, filters_list)[1]
            temp_list1 = crawling(query, filters_list)[3]
            news_data1[query] = news(query)

        for query in list2:
            result3[query] = crawling(query, filters_list)[0]
            # result4[query] = crawling(query, filters_list)[1]
            news_data2[query] = news(query)

        print(temp_list1)

        count_list1 = count_items(result1)
        count_list2 = count_items(result3)

        random.shuffle(colors)
        # print(video_links)
        # print(wiki_links)
        # wikis = wiki_data(list(set(wiki_links)))
        print(wiki_scrape_temp)
        images_updated = list(filter(None, images))

        context = {
            'home': True,
            'userprofile': userprofile,
            'notifications': notifications[:5],
            'unread_count': len(unread),
            'labels': filters_list,
            # 'result1': result2,
            # 'result2': result4,
            'list1': list1,
            'list2': list2,
            'count_list1': count_list1,
            'count_list2': count_list2,
            'temp_list1': temp_list1,
            'random_colors': colors,
            'news_data1': news_data1,
            'news_data2': news_data2,
            'wikis': wiki_scrape_temp,
            'main_search_list': main_search_list,
            'video_links': list(set(video_links))[:5],
            'pdfs': pdfs,
            'scrape_data_dict_main': scrape_data_dict_main,
            'images': images_updated
        }

        return render(request, 'crawler/result.html', context=context)
