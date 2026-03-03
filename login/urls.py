from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    #registro
    path('api/register/', views.UserRegistrationView.as_view(), name='api_register'),
    #login
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
]