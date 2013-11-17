from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import serializers
from django.utils import decorators
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urlparse import urlparse
import urllib2

import os.path
from uuid import uuid4

from motsdits import models


class LoginView(APIView):
    '''Taken from http://stackoverflow.com/questions/17931158/angularjs-django-rest-framework-cors-csrf-cookie-not-showing-up-in-client'''

    renderer_classes = (JSONRenderer, )

    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        '''Perform authentication via AngularJS'''
        serializer = serializers.LoginSerializer(data=request.DATA)
        if serializer.is_valid():
            userAuth = authenticate(username=serializer.data['email'], password=serializer.data['password'])
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


class TempUploadView(APIView):
    '''Performs a temporary file upload'''

    renderer_classes = (JSONRenderer, )

    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request):
        '''Stores an uploaded file in our S3 temp folder'''

        # @TODO: check file size
        # @TODO: Perform the read incrementally to ensure we can't be overwhelmed
        path = default_storage.save(
            'tmp/images/{}.jpg'.format(uuid4()),
            ContentFile(request.FILES['image'].read())
        )

        return Response({'src': os.path.join(settings.MEDIA_URL, path)}, status=status.HTTP_200_OK)


class CreateNewMotDitView(APIView):
    '''Creates a new Mot-dit from the full form, including any opinion / photo object related to it'''

    renderer_classes = (JSONRenderer, )

    @decorators.method_decorator(ensure_csrf_cookie)
    def post(self, request):
        '''Creates a new Mot-dit, with related content'''

        from pprint import pprint
        pprint(request.DATA)

        # @TODO: Form validation and rollback on failure
        motdit = models.MotDit(
            created_by=request.user,
            name=request.DATA['name'],
            website=request.DATA.get('website'),
            address=request.DATA.get('address'),
            category=models.Category.objects.get(id=request.DATA['category']['id'])
        )
        motdit.save()

        # Add the subfilters
        for key, subfilters in request.DATA.get('subfilters', {}).iteritems():
            if not isinstance(subfilters, list):
                subfilters = [subfilters]

            for subfilter in subfilters:
                motdit.subfilters.add(models.Subfilter.objects.get(id=subfilter['id']))

        # Create an opinion object
        if request.DATA.get('opinion').strip():
            opinion = models.Opinion(
                created_by=request.user,
                motdit=motdit,
                text=request.DATA['opinion']
            )
            opinion.save()
            motdit.top_opinion = opinion

        # Create a photo object
        if request.DATA.get('photo').strip():

            url = request.DATA['photo']

            # Thanks to: http://stackoverflow.com/questions/1393202/django-add-image-in-an-imagefield-from-image-url
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(url).read())
            img_temp.flush()

            photo = models.Photo(
                created_by=request.user,
                motdit=motdit
            )

            photo.photo.save(
                urlparse(url).path.split('/')[-1],
                File(img_temp),
                save=True
            )

            motdit.top_photo = photo

        if request.DATA.get('tags').strip():
            for tag_name in map(lambda x: x.strip(), request.DATA['tags'].split(',')):
                tag, created = models.Tag.objects.get_or_create(
                    slug=tag_name.lower(),
                    defaults={'name': tag_name}
                )
                if created:
                    tag.save()
                # finally, add to the motdit
                motdit.tags.add(tag)

        motdit.save()

        return Response({
            'success': True,
            'motdit': serializers.compact.CompactMotDitSerializer(motdit).data
        }, status=status.HTTP_200_OK)
