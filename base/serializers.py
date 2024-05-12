from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mail, Box

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'firstname',
            'lastname',
            'email address',
            'active',
            'staff status', 
            'superuser status',
            'last login',
            'date joined',
        ]

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            'owner',
            'name',
            'numInside',
        ]

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = [
            'id',
            'sender',
            'receiver',
            'currentBox',
            'title',
            'previousMail',
            'content',
            'sentDate',
            'isResponse',
            'isUnread',
            'isSelected',
            'inShadowRealm',
        ]