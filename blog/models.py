from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    autor= models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='static/posts/', blank=True, null=True)
    video = models.FileField(upload_to='static/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo