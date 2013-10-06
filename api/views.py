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

    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        '''Perform authentication via AngularJS'''
        serializer = serializers.LoginSerializer(data=request.DATA)
        if serializer.is_valid():
            userAuth = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if userAuth:
                if userAuth.is_active:
                    login(request, userAuth)
                    user = {'isLogged': True}
            else:
                user = {'isLogged': False}
            return Response(user, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    '''An adaptation of the login view to handle registration'''

    renderer_classes = (JSONRenderer, )

    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        '''Allows for posting of user objects to the api'''
        serializer = serializers.RegisterSerializer(data=request.DATA)

        if serializer.is_valid():
            try:

                if serializer.data['password'] != serializer.data['password2']:
                    raise ValueError("Passwords don't match")

                user = User.objects.create_user(serializer.data['username'], serializer.data['email'], serializer.data['password'])
                user.first_name = serializer.data['firstname']
                user.last_name = serializer.data['lastname']
                # TODO: Add userprofile data
                user.save()
                return Response({'created': True}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'created': False, 'reason': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
