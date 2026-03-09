from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login_page'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    #registro
    path('api/register/', views.UserRegistrationView.as_view(), name='api_register'),
    #login
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    #editar usuario
    path('api/editar/<int:pk>/', views.EditarUsuarioView.as_view(), name='api_editar'),
]