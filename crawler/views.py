from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required
def index(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = dict()
    context['userprofile'] = userprofile
    return render(request, "crawler/index.html", context=context)


@login_required
def test(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = dict()
    context['userprofile'] = userprofile
    return render(request, "crawler/result.html", context=context)
