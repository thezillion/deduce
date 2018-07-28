from rest_framework import serializers
from .models import Level, KryptosUser
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        user = User(**data)
        errors = dict()
        try:
            validators.validate_password(password=data['password'], user=User)
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'])
        user.email =validated_data['email']
        user.set_password(validated_data['password'])
        user.save ()
        return user

    class Meta:
        email = serializers.EmailField(required=True)
        fields = (
            'username',
            'email',
            'password'
        )
        model = User


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'level',
            'answer',
            'source_hint',
        )
        model = Level


class KryptosUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user_id',
            'level',
            'rank',
        )
        model = KryptosUser
