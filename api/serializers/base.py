from rest_framework import serializers
import hashlib
import urllib


class BaseUserSerializer(serializers.ModelSerializer):
    '''Serves a base to User serialization objects to ensure all dynamic attributes can be shared'''

    photo = serializers.SerializerMethodField('get_gravatar')

    def get_gravatar(self, obj):
        '''Generates a gravatar url'''
        # default = "`http://example.com/static/images/defaultavatar.jpg"
        size = 150

        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(obj.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s': str(size)})
        return gravatar_url
