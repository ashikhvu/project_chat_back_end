from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModelsSerializer,UserModelLoginSerializer,RequestSerializer,ShowUserModelsSerializer,ShowRequestSerializer
from .models import UserModel,Request
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated    

class SignUp(APIView):
    def post(self,request):
        serializer = UserModelsSerializer(data=request.data)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        name = first_name+' '+last_name
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        contact = request.data.get('contact')
        image = request.FILES.get('image')

        if serializer.is_valid():
            try:
                user = UserModel.objects.create_user(
                    name = name,
                    first_name = first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email= email,
                    contact=contact,
                    image=image
                )
                token = Token.objects.create(user=user)
                print(token.key)
                return Response(serializer.data)
            except:
                pass
        return Response(serializer.errors)
    
class SignIn(APIView):
    def post(self,request):
        serializer = UserModelLoginSerializer(data=request.data)
        print('outside')
        print(request.data.get('username'))
        print(request.data.get('password'))
        if serializer.is_valid():
            print('inside')
            user = authenticate(
                username = request.data.get('username'),
                password=request.data.get('password')
            )
            if user:
                token = Token.objects.get(user=user)
                print(token.key)
                return JsonResponse({"success":"success","token":token.key})
            else:
                return JsonResponse({"error":"Invalid Login Credential"})
        return Response(serializer.errors)
        
class Home(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        users = UserModel.objects.all()
        if users:
            serializer = ShowUserModelsSerializer(users,many=True)
            return Response(serializer.data)
        return JsonResponse({'error':'no users exists'})
    
class GetUserData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        id = request.GET.get('id')
        if id:
            user = UserModel.objects.get(id=id)
            if user:
                serializer = ShowUserModelsSerializer(user,many=False)
                return Response(serializer.data)
        else:
            user = UserModel.objects.get(username=request.user)
            if user:
                serializer = ShowUserModelsSerializer(user,many=False)
                return Response(serializer.data)
        return JsonResponse({'error':"User Doesn't exist"})
        
class GetAllUserData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        search_text = request.GET.get('search_text')
        print(search_text)
        if search_text:
            user = UserModel.objects.filter(name__icontains=search_text).exclude(username=request.user.username)
            if user:
                serializer = ShowUserModelsSerializer(user,many=True)
                return Response(serializer.data)
        else:
            users = UserModel.objects.filter(is_superuser=False).exclude(username=request.user.username)
            if users:
                serializer = ShowUserModelsSerializer(users,many=True)
                return Response(serializer.data)
        return JsonResponse({'error':"User Doesn't exist"})
        
class SendRequest(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        id = request.GET.get('id')
        print(f'===={id}=====')
        if id:
            user = Request.objects.filter(req_from=id)
            if user:
                serializer = ShowRequestSerializer(user,many=True)
                return Response(serializer.data)
        return JsonResponse({'error':'Give an id'})
    def post(self,request,**kwargs):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)