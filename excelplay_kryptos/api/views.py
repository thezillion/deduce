from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Level, KryptosUser
from .serializers import UserSerializer,ChangePasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_account(request):
    """
    user registration endpoint
    """
    permission_classes = (AllowAny,)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    """
    user login endpoint
    """
    try:
        email = request.data['email']
        password = request.data['password']
        username  = User.objects.get(email=email).username
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'login':True})
        return Response({'login':False}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def logout_user(request):
    """
    user logout endpoint
    """
    logout(request)
    return Response({'logout':True})


# @api_view(['POST'])
# def change_password(request):
#     serializer = ChangePasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         user = request.user
#         if  user.check_password(request.data['old_password']):
#             print('old_password',True)
#             user.set_password(request.data['new_password'])
#             print('new_password set')
#             return Response("success")
#         return Response({"old_password":"wrong"}, status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.errors)
class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

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
            new_password = serializer.data.get("new_password")
            self.object.set_password(new_password)
            self.object.save()
            return Response({"password":["changed"]}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))
def password_reset(request):
    try:
        email = request.data['email']
        print(request.data)

        if len(User.objects.filter(email=email)) != 0:
            form = PasswordResetForm(request.data)
            assert form.is_valid()
            form.save(request=request, from_email="kryptos@excelmec.org", email_template_name='registration/password_reset_email.html')
            return Response('success')
        return Response('Email id not registered', status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response('Email id not registered', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def test(request):
    print(request)
    user = User.objects.get(username = request.user.username)
    response = {'success': True, 'username':user.username,'a':request.site}
    return JsonResponse(response)

@api_view(['GET'])
def ask(request):
    """
    endpoint to provide the current level question
    """

    # TODO: Fetch user level from DB
    user_level = KryptosUser.objects.get(user_id = request.user.id).level
    level = Level.objects.filter(level=user_level)[0]
    response = {
        'level': user_level,
        'source_hint': level.source_hint
    }
    return Response(response)

@api_view(['POST'])
def answer(request):
    """
    endpoint to post the user response
    """
    user_id = request.user.id
    answer = request.data['answer']
    try:
        user = User.objects.get(id=user_id)
        kuser = KryptosUser.objects.get(user_id=user)
        level = Level.objects.get(level=kuser.level)
        print (answer, level.answer)
        if answer == level.answer:
            print(user, " answered level ", kuser.level, " correctly.")
            kuser.level += 1
            kuser.save()
            response = {'answer': 'Correct'}
        else:
            response = {'answer': 'Wrong'}
        return Response(response)
    except Exception as e:
        print (e)
        response = {'error': 'User not found'}
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
