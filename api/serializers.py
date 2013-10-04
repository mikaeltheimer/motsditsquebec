from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    '''Simple serializer for login requests'''
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class LoginResponseSerializer(serializers.Serializer):
    '''Simple response to login serialization'''
    
