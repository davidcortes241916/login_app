from django.shortcuts import render

#serializers
from rest_framework import generics, response, status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth.models import User

#json
from django.http import JsonResponse
import json

#vistas
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

#registro
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

#login
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return JsonResponse({'message': 'Login exitoso'})
        else:
            return JsonResponse({'message': 'Credenciales inválidas'}, status=400)