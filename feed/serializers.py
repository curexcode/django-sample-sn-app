from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Post, Comment, Connection, PendingConnection


class PendingConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingConnection
        fields = ('sender', 'receiver')
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'date', 'image', 'text', 'public', 'likes')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ('post', 'user', 'date', 'image', 'text', 'likes')



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account 
#         fields = ('id', 'name', 'phone_number', 'gender', 'city', 'profile_pic','verified')

# class ChangePasswordSerializer(serializers.Serializer):
#     # class Meta:
#     #     model = Account 
#     #     fields = ('password')
#     model = Account
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)