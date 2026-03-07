from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('crear_post/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post, name='post'),
    path('editar_post/<int:pk>/', views.post_update, name='editar_post'),
    #funciones post DRF
    path('api/crear_post/', views.CrearPostView.as_view(), name='crear_post_api'),
    path('api/posts/', views.PostListView.as_view(), name='posts_api'),
    path('api/post/<int:pk>/', views.PostDetailView.as_view(), name='post_api'),
    path('api/editar_post/<int:pk>/', views.EditarPostView.as_view(), name='editar_post_api'),
]