from rest_framework import serializers
from .models import *

class UserModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

class UserModelLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField()

class ShowUserModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ['password']

class RequestSerializer(serializers.ModelSerializer):
    req_from = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    req_to = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())

    class Meta:
        model = Request
        fields = "__all__"

class ShowRequestSerializer(serializers.ModelSerializer):

    req_from = ShowUserModelsSerializer()
    req_to = UserModelsSerializer()

    class Meta:
        model = Request
        fields = "__all__"

class ChatModelSeralizer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ['from_user','to_user','msg']

class ShowChatModelSeralizer(serializers.ModelSerializer):
    from_user = UserModelsSerializer()
    to_user = UserModelsSerializer()

    class Meta:
        model = ChatModel
        fields = '__all__'