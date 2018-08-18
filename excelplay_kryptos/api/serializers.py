from rest_framework import serializers
from .models import Level, KryptosUser
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class LevelSerializer(serializers.ModelSerializer):
    """
    Serializer for question endpoint
    """
    class Meta:
        fields = (
            'id',
            'level',
            'answer',
            'source_hint',
        )
        model = Level


class KryptosUserSerializer(serializers.ModelSerializer):
    """
    Serializer for KryptosUser Profile
    """
    class Meta:
        fields = (
            'id',
            'user_id',
            'level',
            'rank',
        )
        model = KryptosUser
