from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Level, KryptosUser
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.

# class CreateUserView(CreateAPIView):
#
#     permission_classes = (AllowAny,)
#     model = User
#     serializer_class = UserSerializer

@api_view(['POST'])
def create_account(request):
    permission_classes = (AllowAny,)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        return Response(generate_token(user), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def test(request):
    response = {'success': True}
    return JsonResponse(response)

@api_view(['GET'])
def ask(request):

    # TODO: Fetch user level from DB
    user_level = 1
    level = Level.objects.filter(level=user_level)[0]
    response = {
        'level': user_level,
        'source_hint': level.source_hint
    }
    return JsonResponse(response)

@csrf_exempt
@api_view(['POST'])
def answer(request):
    user_id = request.data['user_id']
    answer = request.data['answer']
    try:
        user = User.objects.get(user_id=user_id)
        kuser = KryptosUser.objects.get(user_id=user)
        level = Level.objects.get(level=kuser.level)
        if answer == level.answer:
            print(user, " answered level ", kuser.level, " correctly.")
            kuser.level += 1
            kuser.save()
            response = {'answer': 'Correct'}
        else:
            response = {'answer': 'Wrong'}
    except Exception as e:
        print (e)
        response = {'error': 'User not found'}
    finally:
        return JsonResponse(response)

def generate_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    print (type(token.key))
    return {"token": token.key}
