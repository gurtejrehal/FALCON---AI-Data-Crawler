from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Notifications
from django.contrib import messages



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
def read(request):

    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)
        notifications = Notifications.objects.filter(user=userprofile)

        for notification in notifications:
            notification.read = True
            notification.save()


        return HttpResponse("0")
