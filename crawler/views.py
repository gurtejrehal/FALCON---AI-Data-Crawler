from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Notifications
from django.contrib import messages
from .crawler_spider import crawling, count_items
import random



@login_required
def index(request):
    userprofile = UserProfile.objects.get(user=request.user)

    notifications = Notifications.objects.filter(user=userprofile)

    unread = notifications.filter(read=False)

    context = dict()
    context['userprofile'] = userprofile
    context['notifications'] = notifications[:5:-1]
    context['unread_count'] = len(unread)

    return render(request, "crawler/index.html", context=context)


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
def read(request):

    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile)

        for notification in notifications:
            notification.read = True
            notification.save()


        return HttpResponse("0")




@login_required
def process(request):

    if request.method == 'POST':

        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile)
        unread = notifications.filter(read=False)


        main_search = request.POST['main_search']
        filters = request.POST['multiple_select']
        print(type(main_search), type(filters))

        main_search_list = [ x.strip(' ') for x in main_search.split(',')]
        filters_list = [x.strip(' ') for x in filters.split(',')]

        result1 = dict()
        result2 = dict()
        result3 = dict()
        result4 = dict()
        list1 = list()
        list2 = list()
        temp_list1 = list()
        colors = ['#111', '#f59042', '#555644', '#444']

        # print(result1)


        # print(count_list)

        if len(main_search_list)>2:
            list1 = main_search_list[:2]
            list2 = main_search_list[3:]

        else:
            list1 = main_search_list


        for query in list1:
            result1[query] = crawling(query, filters_list)[0]
            result2[query] = crawling(query, filters_list)[1]
            temp_list1 = crawling(query, filters_list)[1]

        for query in list2:
            result3[query] = crawling(query, filters_list)[0]
            result4[query] = crawling(query, filters_list)[1]

        count_list1 = count_items(result1)
        count_list2 = count_items(result3)

        random.shuffle(colors)

        print(count_list1)

        context = {
            'userprofile': userprofile,
            'notifications': notifications[:5:-1],
            'unread_count': len(unread),
            'labels': filters_list,
            'result1': result2,
            'result2': result4,
            'list1': list1,
            'list2': list2,
            'count_list1': count_list1,
            'count_list2': count_list2,
            'temp_list1': temp_list1,
            'random_colors': colors
        }

        return render(request, 'crawler/result.html', context=context)


