from django.conf import settings

from django.shortcuts import render
from django.http import JsonResponse
from .models import Level, KryptosUser, Profile
from .serializers import SocialSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from requests.exceptions import HTTPError
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from social_django.utils import psa
# Create your views here.

@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):

    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user:
            if user.is_active:
                # token, _ = Token.objects.get_or_create(user=user)
                # return Response({'token': token.key})
                login(request=request, user=user)
                return Response({'login':True})
            else:
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

def user_logout(request):
    logout(request)
    return JsonResponse({'logout':True})

def test(request):
    response = {'success': KryptosUser.objects.all()[0].user_id.email}
    return JsonResponse(response)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    first_name = profile.user_id.first_name
    last_name = profile.user_id.last_name
    email = profile.user_id.email
    profile_picture = profile.profile_picture
    return Response({'first name':first_name,
    'last name':last_name,
    'email':email,
    'profle':profile_picture})

@api_view(['GET'])
def ask(request):

    user_level = KryptosUser.objects.get(user_id=request.user.id).level
    level = Level.objects.filter(level=user_level)[0]
    try:
        level = Level.objects.filter(level=user_level)[0]
        site = request.META['HTTP_HOST']
        file = ""
        image = ""
        if level.level_file: file=level.level_file.url
        if level.level_image: image=level.level_image.url
        response = {
            'level': user_level,
            'source_hint': level.source_hint,
            'data_type': level.filetype,
            'data_url': file,
            'image': image,
            'timestamp':timezone.now()
        }
        return Response(response)
    except Exception as e:
        print (e)
        return Response({"level":"finished"})

@api_view(['POST'])
def answer(request):
    answer = request.data['answer']
    try:
        user = User.objects.get(id=request.user.id)
        kuser = KryptosUser.objects.get(user_id=user)
        level = Level.objects.get(level=kuser.level)
        if answer.lower() == level.answer.lower():
            kuser.level += 1
            kuser.save()
            response = {'answer': 'Correct'}
        else:
            response = {'answer': 'Wrong'}
    except Exception as e:
        print (e)
        response = {'error': 'User not found'}
    finally:
        return Response(response)


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    leaderboard = []
    users = KryptosUser.objects.all()
    for row, user in enumerate(users):
        username = user.user_id.username
        name = user.user_id.first_name + " " + user.user_id.last_name
        leaderboard.append({
        "username":username,
        "rank":row+1,
        "name":name,
        "level":user.level})
    return Response({"leaderboard":leaderboard})

@api_view(['GET'])
def user_rank(request):
    users = KryptosUser.objects.all()
    for row, user in enumerate(users):
        if user.user_id.username == request.user.username:
            return Response({'rank':row+1})
