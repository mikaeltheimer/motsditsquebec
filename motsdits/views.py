from django.shortcuts import render


def example_view(request):
    '''Simply renders example.html'''
    return render(request, 'example.html')
