from django.shortcuts import render
from django.http import HttpResponse
from account.serializers import UserSerializer,RegisterSerializer
from account.models import Account
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions 



# class UserSerializer(serializers.ModelSerializer):


@api_view(['GET'])
def api_overview(req):
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


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

    
