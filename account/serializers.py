from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Account 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account 
        fields = ('id', 'name', 'phone_number', 'gender', 'city', 'profile_pic','verified')

class ChangePasswordSerializer(serializers.Serializer):
    # class Meta:
    #     model = Account 
    #     fields = ('password')
    model = Account
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Account 
        fields = ('name', 'phone_number', 'gender', 'city', 'profile_pic')
        # extra_kwargs = {'password': {'write_only': True}}
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Account 
        fields = ('id', 'name', 'phone_number', 'gender', 'city', 'profile_pic', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = Account.objects.create_user(validated_data['name'], validated_data['phone_number'], 
validated_data['gender'], validated_data['city'], validated_data['profile_pic'],validated_data['password'])
        return user