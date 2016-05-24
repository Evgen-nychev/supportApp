from rest_framework import serializers
from .models import Message, User, Otdel

class OtdelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otdel

class UserSerializer(serializers.ModelSerializer):
    otdel = OtdelSerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'otdel', 'is_staff')

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Message
