from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

#autenticación de usuarios
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Usuario no encontrado.")

        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")

        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")

        data["user"] = user
        return data
        
#crear un serializer para el usuario
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False  # Desactiva el usuario hasta que se confirme el correo
        user.save()

        return user

#actualizar usuario
class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("El usuario ya existe")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("El email ya existe")
        return value
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        password2 = validated_data.pop("password2", None)

        if password and password2:
            if password != password2:
                raise serializers.ValidationError("Las contraseñas no coinciden")
            instance.set_password(password)

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        instance.save()
        return instance

#eliminar usuario