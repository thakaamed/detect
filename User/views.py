from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


@csrf_exempt
@api_view(['POST'])
def obtain_token(request):
    print("request.post", request.POST)
    # Kullanıcı adı ve şifre al
    username = request.data.get('username')
    password = request.data.get('password')
    print("username", username)
    print("password", password)


    # Kullanıcıyı doğrula ve token oluştur
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@csrf_exempt
@api_view(['POST'])
def verify_token(request):
    print("request.post", request.POST)
    # Kullanıcı adı ve şifre al
    token = request.data.get('token')
    print("token", token)

    # Kullanıcıyı doğrula ve token oluştur
    user_dict = {}
    user_with_token = Token.objects.filter(key=token).first()
    if user_with_token:
        user = user_with_token.user
        user_dict["username"] = user.username
        user_dict["email"] = user.email
        user_dict["name"] = user.first_name
        user_dict["roles"] = "monailabel-user#monailabel-admin#monailabel-reviewer#monailabel-annotator"
        print("user_dict", user_dict)  # Diğer bilgiler
        return Response({'user_dict': user_dict})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

# Create your views here.


def beartoken(request):
    return JsonResponse({"status": True})