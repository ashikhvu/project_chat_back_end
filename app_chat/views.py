from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserModelsSerializer,UserModelLoginSerializer,RequestSerializer,ShowUserModelsSerializer,ShowRequestSerializer,ChatModelSeralizer,ShowChatModelSeralizer
from .models import UserModel,Request,ChatModel
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated    
from django.db.models import Q

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
            user = UserModel.objects.get(id=request.user.id)
            if user:
                serializer = ShowUserModelsSerializer(user,many=False)
                return Response(serializer.data)
        return JsonResponse({'error':"User Doesn't exist"})
        
class GetAllUserData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        search_text = request.GET.get('search_text')
        # print(search_text)
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
    def get(self, request, **kwargs):
        req_from = request.GET.get('req_from')
        req_to = request.GET.get('req_to')
        if req_from and req_to:
            req_data = None
            try:
                req_data1 = Request.objects.get(req_from=req_from, req_to=req_to)
                req_data = req_data1
            except Request.DoesNotExist:
                pass
            if not req_data:
                try:
                    req_data2 = Request.objects.get(req_from=req_to, req_to=req_from)
                    req_data = req_data2
                except Request.DoesNotExist:
                    pass
            if req_data:
                serializer = ShowRequestSerializer(req_data)
                print(serializer.data['status'])
                return Response(serializer.data)
            return Response({"error": "Request doesn't exist."})
        return Response({"error": "Missing required parameters."})
        
    
    def post(self,request,**kwargs):
        req_from = request.data.get('req_from')
        req_to = request.data.get('req_to')
        print(f'send_request from={req_from} to={req_to}')
        existing_request1 = Request.objects.filter(req_from=req_from, req_to=req_to).first()
        existing_request2 = Request.objects.filter(req_from=req_to, req_to=req_from).first()
        if existing_request1 or existing_request2:
            return Response({'error': 'Request already exists'}, status=400)
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    
    def put(self,request,**kwargs):
        req_from= request.data.get('req_from')
        req_to= request.data.get('req_to')
        if req_from and req_to:
            print(f'accept_request from={req_from} to={req_to}')
            try:
                print('1')
                request_data = Request.objects.filter(req_from=req_to,req_to=req_from).first()
                print('2')
                if request_data:
                    print('3')
                    print('data here')
                    serializer = RequestSerializer(instance=request_data,data=request.data,partial=True)
                    if serializer.is_valid():
                        print('valid')
                        serializer.save()
                        return JsonResponse({"success":"Request Status Changed"})
                    else:
                        print('not valid')
                        return JsonResponse({"error":"not valid"})
            except:
                pass
        return JsonResponse({"error":"Request Status Change Failed."})
    
    def delete(self,request,**kwargs):
        req_from= request.data.get('req_from')
        req_to= request.data.get('req_to')
        print(f'{req_from} {req_to}')
        if req_from and req_to:
            print('valid')
            try:
                request_data = Request.objects.filter(req_from=req_from,req_to=req_to)
                if request_data:
                    request_data.delete()
                    return JsonResponse({"success":"Request Cancelled"})
            except:
                pass
        return JsonResponse({"error":"Request doesn't exist."})
        
class RequestContact(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,**kwargs):
        id = request.GET.get('id')
        print(f'get all the request of={id}')
        if id:    #get multiple requests
            print('request_contact')
            try:
                req_data = Request.objects.filter(req_to=id).exclude(status='accepted').values_list('req_from',flat=True)
                req_contacts = UserModel.objects.filter(id__in=req_data)
                if req_data:
                    serializer = UserModelsSerializer(req_contacts,many=True)
                    return Response(serializer.data)
                return JsonResponse({'error':"request diesn't exist"})
            except:
                pass
        return JsonResponse({'error':'Give an id'})

class ChatMessages(APIView):
    def post(self,request,**kwargs):
        print('send_msg')
        serializer = ChatModelSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    def get(self,request,**kwargs):
        print('get_msg')
        from_user= request.GET.get('from_user')
        to_user= request.GET.get('to_user')
        print(f'{from_user} {to_user}')
        if from_user and to_user:
            try:
                all_messages = ChatModel.objects.filter(Q(from_user=from_user,to_user=to_user)|Q(from_user=to_user,to_user=from_user)).order_by('create_at')
            except:
                pass
            if all_messages.exists():
                serializer = ShowChatModelSeralizer(all_messages,many=True)
                return Response(serializer.data,status=201)
            return Response({'error':"messages doesn't exist"},status=400)
        return Response({'error':'request failed'},status=400)