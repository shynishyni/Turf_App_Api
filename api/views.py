from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import UserSreializer
from .serializers import TurfSerializer
from .serializers import TurfImageSerializer
from django.http.response import JsonResponse
from .models import UserDetailsTable
from .models import TurfDetails
from .models import TurfImage
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import json

@csrf_exempt
def user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['password'] = make_password(data['password'])
        serializer = UserSreializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User Data added successfully"}, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)
    if request.method == 'GET':
        item= UserDetailsTable.objects.all()
        serializer = UserSreializer(item,many=True)
        return JsonResponse(serializer.data,safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')
        password = data.get('password')
        print(identifier, password)
        try:
            user = UserDetailsTable.objects.filter(email=identifier).first() or \
                   UserDetailsTable.objects.filter(phone=identifier).first()
            if user:   
                if check_password(password, user.password):
                    return JsonResponse({"message": "Login successful"}, safe=False)
                else:         
                    return JsonResponse({"error": "Invalid credentials"}, status=401, safe=False)
            else:      
                return JsonResponse({"error": "Invalid credentials"}, status=401, safe=False) 
        except Exception as e:        
            return JsonResponse({"error": str(e)}, status=500, safe=False)  
    return JsonResponse({"error": "Invalid request method"}, status=405, safe=False)

@csrf_exempt
def turf(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            data = json.loads(request.body)
            serializer = TurfSerializer(data=data)
            if serializer.is_valid():
                turf_instance = serializer.save()
                for image in request.FILES.getlist('image'):
                    TurfImage.objects.create(turf=turf_instance, image=image)
                return JsonResponse({"message": "Turf Data added successfully"}, safe=False)
            else:
                return JsonResponse(serializer.errors, safe=False)
    if request.method == 'GET':
        item= TurfDetails.objects.all()
        serializer = TurfSerializer(item,many=True)
        return JsonResponse(serializer.data,safe=False)
@csrf_exempt
def update_turf(request,turf_name=""):
    data = JSONParser().parse(request)
    try:
        item = TurfDetails.objects.get(turf_name=turf_name)
        serializer = TurfSerializer(item, data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Updated Successfully"}, safe=False)
        return JsonResponse({"message": "Failed to Update"}, safe=False)
    except TurfDetails.DoesNotExist:
         return JsonResponse({"message": "Item not found"}, status=404)
