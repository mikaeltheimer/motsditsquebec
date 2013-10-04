from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import serializers
from django.utils import decorators
from django.views.decorators.csrf import ensure_csrf_cookie


class LoginView(APIView):
    '''Taken from http://stackoverflow.com/questions/17931158/angularjs-django-rest-framework-cors-csrf-cookie-not-showing-up-in-client'''

    renderer_classes = (JSONRenderer, )

    # TODO: Make this work
    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        '''Perform authentication via AngularJS'''
        serializer = serializers.LoginSerializer(data=request.DATA)

        if serializer.is_valid():
            userAuth = authenticate(username=serializer.data['username'], password=serializer.data['password'])

            if userAuth:

                if userAuth.is_active:
                    login(request, userAuth)
                    loggedInUser = User.objects.get(pk=1)
                    serializer = serializers.LoginResponseSerializer(loggedInUser)

                    user = [serializer.data, {'isLogged': True}]

            else:
                user = {'isLogged': False}

            return Response(user, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
