from django.shortcuts import render, redirect

#serializers
from rest_framework import generics, response, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, get_user_model, logout
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth.models import User

#json
from django.http import JsonResponse
from rest_framework.response import Response
import json

#vistas
def login_page(request):
    return render(request, 'socialaccount/login.html')

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html')

#registro
class UserRegistrationView(generics.CreateAPIView): #para registrar se usa CreateAPIView
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

#login
User= get_user_model()
class UserLoginView(generics.GenericAPIView):
    def post(self, request): #se define el método post para recibir los datos de login
        serializer = UserSerializer(
            data=request.data,#se pasan los datos del request al serializer para que los valide
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)#se loguea al usuario
            return Response({"success": True})#se devuelve una respuesta de éxito

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST #si el serializer no es válido se devuelve un error 400 con los errores del serializer
        )
        
#logout
def logout_view(request):
    logout(request)
    return redirect('/')