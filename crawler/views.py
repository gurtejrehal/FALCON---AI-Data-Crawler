from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Notifications, Keyword, Category, Link, CrawledLinks
from django.contrib import messages
from utils.crawler_spider import crawling, count_items, wiki_data, wiki_scraping
from utils.news import news
from utils.analytics import category_percent, category_count, keyword_trends
import random, copy
from django.http import JsonResponse
from django.db.models import Count


@login_required
def index(request):
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
def test(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = dict()
    context['userprofile'] = userprofile
    return render(request, "crawler/result.html", context=context)


@login_required
def update(request):
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
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        keyword = str(request.POST['keyword'])
        content = f"Report is being generated for '{keyword}'"
        notification = Notifications(user=userprofile, content=content)
        notification.save()

        return HttpResponse("1")


@login_required
def update_notifications_base(request):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')

        context = {
            'notifications': notifications[:5]
        }

        return render(None, "crawler/update_notifications.html", context=context)


@login_required
def read(request):
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile)

        for notification in notifications:
            notification.read = True
            notification.save()

        return HttpResponse("0")


def api(request, keyword):
    result = news(keyword)

    data = {
        keyword: result
    }
    return JsonResponse(data)


@login_required
def process(request):
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
        scrape_data = ""
        no_of_links = 0
        no_of_scrape = 0
        wiki_scrape_temp = dict()
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

                    if "wikipedia" in link:
                        scrape_data, empty = wiki_scraping(link)
                        no_of_scrape += 1
                        wiki_links.append(link)
                        if not empty:
                            wiki_scrape_temp[str(link)] = scrape_data

                    elif "youtube" in link:
                        video_links.append(link)

                    link = Link.objects.get_or_create(keyword=query, category=cat, link=link, scrape_data=scrape_data)[0]
                    link.save()

                    profile_update, created = CrawledLinks.objects.get_or_create(userprofile=userprofile,
                                                                                 link=link, reschedule=reschedule_crawler)
                    profile_update.save()

                    if created:
                        no_of_links += 1

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
            temp_list1 = crawling(query, filters_list)[1]
            news_data1[query] = news(query)

        for query in list2:
            result3[query] = crawling(query, filters_list)[0]
            # result4[query] = crawling(query, filters_list)[1]
            news_data2[query] = news(query)

        count_list1 = count_items(result1)
        count_list2 = count_items(result3)

        random.shuffle(colors)
        print(video_links)
        print(wiki_links)
        # wikis = wiki_data(list(set(wiki_links)))
        print(wiki_scrape_temp)

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
            'video_links': list(set(video_links))[:5]
        }

        return render(request, 'crawler/result.html', context=context)
