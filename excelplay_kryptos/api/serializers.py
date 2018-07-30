from rest_framework import serializers
from .models import Level, KryptosUser
from django.contrib.auth.models import User
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration endpoint
    """
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    #first_name = serializers.CharField(required=True)
    #last_name = serializers.CharField(required=True)

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
            'password',
            'first_name',
            'last_name'
        )
        model = User

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate(self, data):
        errors = dict()
        try:
            validators.validate_password(password=data['new_password'], user=User)
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(ChangePasswordSerializer, self).validate(data)




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
