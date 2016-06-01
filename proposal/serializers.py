from rest_framework import serializers
from .models import Message, User, Otdel, Vajnost, Status, Tema, Tip, SupportRecuest, ConfugurationOneC

class ConfugurationOneCSerializaer(serializers.ModelSerializer):
    class Meta:
        model = ConfugurationOneC

class OtdelSerializer(serializers.ModelSerializer):
    configuration_1c = ConfugurationOneCSerializaer(many=True, read_only=True)
    class Meta:
        model = Otdel

class UserSerializer(serializers.ModelSerializer):
    otdel = OtdelSerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'last_name', 'otdel', 'is_staff')

class VajnostSeriz(serializers.ModelSerializer):
    class Meta:
        model = Vajnost

class StatusSeriz(serializers.ModelSerializer):
    class Meta:
        model = Status

class TemaSeriz(serializers.ModelSerializer):
    class Meta:
        model = Tema

class TipSeriz(serializers.ModelSerializer):
    class Meta:
        model = Tip

class SupportRecuestSerializer(serializers.ModelSerializer):
    creator = UserSerializer()
    type = TipSeriz()
    vajnost = VajnostSeriz()
    status = StatusSeriz()
    tema = TemaSeriz()
    configuration_1c = ConfugurationOneCSerializaer()
    class Meta:
        model = SupportRecuest

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Message
