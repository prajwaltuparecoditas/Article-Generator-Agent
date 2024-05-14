from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication,  TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .models import User
from .agent import agent_with_history

# API to sign up a new user
class UserRegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'success': True,
                'user': serializer.data,
                'token': Token.objects.get(user=User.objects.get(username=serializer.data['username'])).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)
    
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            response = {
                "username":{
                    "detail": "User Does not exist"
                }
            }

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request,user)
                 
                token,created = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        print(request.user.id)
        token = Token.objects.get(user_id=request.user.id)
        logout(request)
        token.delete()

        return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)

class GenerateArticleAPI(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_input = request.POST.get('query')
        result = agent_with_history.invoke({"input": user_input}, {"configurable":{"session_id":request.session.session_key}},)
        return Response({"AI response":result["output"]})