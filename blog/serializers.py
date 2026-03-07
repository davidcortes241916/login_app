from rest_framework import serializers
from .models import Post

#crear un serializer para el modelo Post
class PostSerializer(serializers.ModelSerializer):#este serializer es para crear y actualizar posts, por eso se usa ModelSerializer que ya tiene implementados los métodos create y update
    autor=serializers.StringRelatedField(read_only=True) #esto es para mostrar el nombre del autor en lugar de su id, read_only=True es para que no se pueda modificar el autor al crear o actualizar un post
    can_delete=serializers.SerializerMethodField() #esto es para mostrar un campo adicional que indique si el post se puede eliminar o no, se usará en el frontend para mostrar o ocultar el botón de eliminar

    class Meta:
        model = Post
        fields = ['id', 'autor', 'titulo', 'contenido', 'imagen', 'video', 'created_at', 'can_delete'] #estos son los campos que se mostrarán en el serializer, se incluye el campo can_delete que es un campo adicional que se calculará con el método get_can_delete
        
    def get_can_delete(self, obj):
        request= self.context.get('request')  # Lógica para determinar si el post se puede eliminar

        if request and request.user == obj.autor:  # Solo el autor del post puede eliminarlo
            return True

        return False 

    def validate(self, data):
        if not data.get('titulo'):
            raise serializers.ValidationError('El título es obligatorio')
        if not data.get('contenido'):
            raise serializers.ValidationError('El contenido es obligatorio')
        return data
        
    def create(self, validated_data):
        user= self.context['request'].user #obtenemos el usuario que hizo la solicitud desde el contexto del serializer
        post = Post.objects.create(autor=user,**validated_data)#crea un nuevo post con los datos validados
        #validated_data es un diccionario con los datos del post, por eso se usa ** para pasar los datos como argumentos al método create
        return post

#mostrar los posts en el home
class viewsSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)  # O usar autor.username
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'autor', 'titulo', 'contenido', 'imagen', 'video', 'created_at', 'can_delete']

    def get_can_delete(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.autor
    
#mostrar un post en detalle
class PostDetailSerializer(serializers.ModelSerializer):
    autor = serializers.CharField(source='autor.username', read_only=True)  # Mostrar el nombre de usuario del autor

    class Meta:
        model = Post
        fields = ['id', 'autor', 'titulo', 'contenido', 'imagen', 'video', 'created_at']

#editar post
class EditarPostSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'autor', 'titulo', 'contenido', 'imagen', 'video', 'created_at']

    def update(self, instance, validated_data):
        for field in ['titulo', 'contenido', 'imagen', 'video']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance

#eliminar post