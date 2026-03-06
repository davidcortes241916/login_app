from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('crear_post/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post, name='post'),
    #funciones post DRF
    path('api/crear_post/', views.CrearPostView.as_view(), name='crear_post_api'),
    path('api/posts/', views.PostListView.as_view(), name='posts_api'),
]