from rest_framework import serializers
from .models import Message, User, Otdel, Vajnost, Status, Tema, Tip, SupportRecuest

class OtdelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otdel

class UserSerializer(serializers.ModelSerializer):
    otdel = OtdelSerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'otdel', 'is_staff')

class VajnostSeriz(serializers.ModelSerializer):
    class Meta:
        model = Vajnost

class StatusSeriz(serializers.ModelSerializer):
    class Meta:
        model = Status

class TemaSeriz(serializers.ModelSerializer):
    class Meata:
        model = Tema

class TipSeriz(serializers.ModelSerializer):
    class Meta:
        model = Tip

class SupportRecuestSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    class Meta:
        model = SupportRecuest

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Message
