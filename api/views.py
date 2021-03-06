from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login
from account.serializers import UserSerializer,RegisterSerializer, ChangePasswordSerializer, UpdateProfileSerializer
from feed.serializers import PostSerializer, CommentSerializer, PendingConnectionSerializer
from account.models import Account
from rest_framework.renderers import JSONRenderer, MultiPartRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions 
from knox.views import LoginView as KnoxLoginView
from feed.models import PendingConnection, Connection, Post, Comment
import json

# class UserSerializer(serializers.ModelSerializer):


@api_view(['GET'])
def api_overview(req):
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def add_friend(req, user_id):
    # current_user_id = 
    pc_obj = PendingConnection.add_pending_request(6, user_id)
    serializer = PendingConnectionSerializer(pc_obj, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def approve_request(req, user_id):
    try:
        pc_obj = PendingConnection.approve_request(user_id,5)         #user_id, req.user.id)
        serializer = PendingConnectionSerializer(pc_obj, many=False)
        return Response(serializer.data)
    except:
        return JsonResponse({'Error': 'Error approving friend request'})
    # return JsonResponse({'Success': 'Friend request accepted of user Id : {0}'.format(user_id))

@api_view(['GET'])
def remove_friend(req, user_id):
    Connection.remove_friend(5, user_id)
    accounts = Connection.get_friends(1)        # replace this with req.user.id
    serializer = UserSerializer(accounts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_friend(req, gender, city, search_str):

    if gender == 'any' and city== 'any':
        users = Account.objects.all()
    elif gender in ['male', 'female']:
        users = Account.objects.filter(gender=gender)
        if city != 'any':               # If city is any then we will consider it as search by gender
            users = Account.objects.filter(city=city)
    else:
        return JsonResponse({'Error': 'Gender params invalid.'})
    
    filtered_users = users.filter(name=search_str)
    if not filtered_users:
        phone_num = '+' + search_str
        filtered_users = users.filter(phone_number=phone_num)

    serializer = UserSerializer(filtered_users, many=True)
    # return JsonResponse({'search_str': search_str, 'filter': filter, 'filter_param':filter_param})

    return Response(serializer.data)

@api_view(['GET'])
def get_pending_requests(req):
    pc_obj = PendingConnection.get_pending_requests(4)
    serializer = PendingConnectionSerializer(pc_obj, many=True)
    return Response(serializer.data)


#Get profile of a specific user
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def get_profile(req, user_id):
    try:
        user = Account.objects.get(pk=user_id)
    except:
        return JsonResponse({'Error': 'There is no user with user ID {0}'.format(user_id)})

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_friends(req, user_id):
    try:
        accounts = Connection.get_friends(user_id)
    except:
        return JsonResponse({'Error': "You don't have any friends yet."})

    serializer = UserSerializer(accounts, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def get_feed(req, user_id):
    try:
        all_posts = Post.objects.filter(user=Account.objects.get(pk=user_id))
    except:
        return JsonResponse({"Error": "No post found from user ID {0}".format(user_id)})
    posts = PostSerializer(all_posts, many=True)
    return Response(posts.data)

# @renderer_classes([MultiPartRenderer])
# @api_view(['POST'])
# def add_new_post(req):
#     serializer = PostSerializer(data=req.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewPostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({
        "Post": PostSerializer(data, context=self.get_serializer_context()).data,
        })

class NewCommentAPI(generics.GenericAPIView):
    serializer_class = CommentSerializer 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({
        "Comment": CommentSerializer(data, context=self.get_serializer_context()).data,
        })

@api_view(['GET'])
def get_comments(req, post_id):
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def like_post(req, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes += 1
    post.save()
    # import pdb; pdb.set_trace()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
def like_comment(req, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.likes += 1
    comment.save()
    # import pdb; pdb.set_trace()
    serializer = CommentSerializer(comment , many=False)
    return Response(serializer.data)

@api_view(['GET']) 
def current_user_feed(req):
    try:
        all_posts = Post.objects.filter(user=Account.objects.get(pk=req.user.id))
    except:
        return JsonResponse({"Error": "No post found from you"})
    posts = PostSerializer(all_posts, many=True)
    return Response(posts.data)

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