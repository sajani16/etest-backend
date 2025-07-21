from rest_framework import serializers
from .models import  User

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']


        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name= first_name,
            last_name = last_name

        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField() 



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']





