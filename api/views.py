from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from account.serializers import UserSerializer,RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer
from account.models import Account
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions 
from knox.views import LoginView as KnoxLoginView
import json



# class UserSerializer(serializers.ModelSerializer):


@api_view(['GET'])
def api_overview(req):
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    model = Account
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # import pdb; pdb.set_trace()
            self.object.name = serializer.data.get('name')
            self.object.phone_number = serializer.data.get('phone_number')
            self.object.gender = serializer.data.get('gender')
            self.object.city = serializer.data.get('city')
            self.object.profile_pic = serializer.data.get('profile_pic')
            self.object.save()

            user = {
                'name':self.object.name ,
                'phone_number': serializer.data.get('phone_number'),
                'gender': self.object.gender,
                'city': self.object.city,
                'profile_pic': serializer.data.get('profile_pic') 
            }
            return Response(json.dumps(user))
        return Response("Error") 

    # def update(self, request, *args, **kwargs):
    #     #self.object is user object
    #     self.object = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         if not self.object.check_password(serializer.data.get("old_password")):
    #             return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
    #         self.object.set_password(serializer.data.get("new_password"))
    #         self.object.save()
    #         response = {
    #             'status': 'success',
    #             'code': status.HTTP_200_OK,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }

    #         return Response(response)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        #self.object is user object
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        # "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)