from django.shortcuts import render


def defaultview(request, template):
    '''Simply renders example.html'''
    return render(request, '{}.html'.format(template))
