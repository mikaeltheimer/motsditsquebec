from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import logout as do_logout


def homepage(request):
    '''Simply renders example.html'''
    return render(request, 'example.html')


def login(request):
    '''Simple login view, redirects the user if they're already authenticated'''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('motsdits.views.homepage'))
    else:
        return render(request, 'login.html')


def logout(request):
    '''Log the user out'''
    do_logout(request)
    return HttpResponseRedirect(reverse('motsdits.views.homepage'))
