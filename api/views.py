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
from rest_framework import status
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
# @csrf_exempt
# def update_turf(request,turf_name=""):
#     if request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         try:
#             item = TurfDetails.objects.get(turf_name=turf_name)
#         except TurfDetails.DoesNotExist:
#             return JsonResponse({"message": "Item not found"}, status=404)
#         data = request.POST.dict()
#         image_files = request.FILES.getlist('image')
#         print("Received data:", data)
#         print("Received files:", request.FILES)
#         serializer = TurfSerializer(item, data = data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             print("Turf details updated:", serializer.data)
#             for image in image_files:
#                 turf_image = TurfImage(turf=item, image=image)
#                 turf_image.save()
#             return JsonResponse({"message": "Updated Successfully"}, safe=False)
#         return JsonResponse({"message": "Failed to Update", "errors": serializer.errors}, safe=False)
    
@csrf_exempt
def update_turf(request, turf_name=""):
    if request.method == 'PUT':
        try:
            # Find the item by turf_name
            item = TurfDetails.objects.get(turf_name=turf_name)
        except TurfDetails.DoesNotExist:
            return JsonResponse({"message": "Item not found"}, status=404)

        # For multipart form-data, use request.POST and request.FILES
        data = request.POST.dict()  # Non-file data
        image_files = request.FILES.getlist('image')  # File data

        # DEBUG: Confirm the received data and files
        print("Received data:", data)
        print("Received files:", request.FILES)

        # Update the TurfDetails instance with partial data
        serializer = TurfSerializer(item, data=data, partial=True)

        if serializer.is_valid():
            # Save the updated data in TurfDetails
            serializer.save()

            # Handle image uploads and associate them with the turf
            for image in image_files:
                # Create a new TurfImage entry for each uploaded image
                turf_image = TurfImage(turf=item, image=image)
                turf_image.save()

            return JsonResponse({"message": "Updated Successfully"}, status=status.HTTP_200_OK)
        else:
            print("Serializer errors:", serializer.errors)
            return JsonResponse({"message": "Failed to Update", "errors": serializer.errors}, safe=False)

    return JsonResponse({"message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)