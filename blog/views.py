from django.shortcuts import render
from rest_framework import generics, response, status
from rest_framework.views import APIView

#post
from .models import Post
from .serializers import PostSerializer, viewsSerializer

#vistas post
def post_create(request):
    return render(request, 'post_create.html')

def post(request, pk):
    return render(request, 'post.html')

#serializers
class CrearPostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request}) #pasamos el request al contexto del serializer para poder acceder al usuario que hizo la solicitud en el método create del serializer
        if serializer.is_valid():
            post = serializer.save()
            return response.Response({'message': 'Post creado exitosamente', 'post': PostSerializer(post).data}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#mostrar los posts en el home    
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = viewsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})  # Agregar el request al contexto del serializer
        return context

#actualizar
#eliminar