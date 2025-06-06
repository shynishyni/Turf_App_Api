from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer
from .serializers import TurfSerializer
from .serializers import TurfBookingDetailsSerializer
from django.http.response import JsonResponse
from .models import UserDetailsTable
from .models import TurfDetails
from .models import TurfBookingDetails
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from geopy.distance import geodesic
from django.shortcuts import render
import json
from django.core.files.base import ContentFile
import base64

@csrf_exempt
def user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data['password'] = make_password(data['password'])
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({"message": "User Data added successfully", "user_id": user.user_id}, status=201)  # Changed to 201 for created
        else:
            return JsonResponse(serializer.errors, safe=False, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

    # if request.method == 'GET':
    #     item= UserDetailsTable.objects.all()
    #     serializer = UserSreializer(item,many=True)
    #     return JsonResponse(serializer.data,safe=False)

@csrf_exempt
def default(request):
    if request.method == 'GET':
          return render(request,'default.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            identifier = data.get('identifier')
            password = data.get('password')

            # Log the incoming data for debugging
            print(f"Received identifier: {identifier}, password: {password}")

            # Check for missing fields
            if not identifier or not password:
                return JsonResponse({"error": "Identifier and password are required"}, status=400)

            user = UserDetailsTable.objects.filter(email=identifier).first() or \
                   UserDetailsTable.objects.filter(phone=identifier).first()

            if user:
                # Log the user found
                print(f"User found: {user.email if user.email else user.phone}")

                if check_password(password, user.password):
                    return JsonResponse({"message": "Login successful", "user_id": user.user_id}, safe=False)
                else:
                    print("Invalid password provided")
                    return JsonResponse({"error": "Invalid credentials"}, status=401, safe=False)
            else:
                print("No user found with the provided identifier")
                return JsonResponse({"error": "User not found"}, status=404, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400, safe=False)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405, safe=False)

    
@csrf_exempt
def getturf(request, id=0):
    if request.method == "GET":
        if id == 0:
            return JsonResponse({"message": "No such turf :("}, status=404)
        else:
            try:
                turf = TurfDetails.objects.get(id=id)
                serializer = TurfSerializer(turf)
                return JsonResponse(serializer.data, safe=False)
            except TurfDetails.DoesNotExist:
                return JsonResponse({"message": "No such turf :("}, status=404)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
            
@csrf_exempt
def getloc(request, lat=0, long=0):
    lat = float(lat) 
    long = float(long) 
    if request.method == "GET":
        if lat == 0 or long == 0:
            return JsonResponse({"message": "Invalid request method"}, status=404)        
        turfs = TurfDetails.objects.all()
        nearby_turfs = []

        for turf in turfs:
            turf_location = (turf.turf_latitude, turf.turf_longitude)
            user_location = (lat, long)
            distance = geodesic(user_location, turf_location).kilometers
            
            if distance <= 5: 
                turf_data = {
                    "turf_name": turf.turf_name,
                    "turf_address": turf.turf_address,
                    "turf_city": turf.turf_city,
                    "turf_state": turf.turf_state,
                    "turf_zip_code": turf.turf_zip_code,
                    "turf_latitude": turf.turf_latitude,
                    "turf_longitude": turf.turf_longitude,
                    "turf_type": turf.turf_type,
                    "surface_type": turf.surface_type,
                    "size": turf.size,
                    "capacity": turf.capacity,
                    "status": turf.status,
                    "opening_time": turf.opening_time,
                    "closing_time": turf.closing_time,
                    "closed_days": turf.closed_days,
                    "hourly_rate": turf.hourly_rate,
                    "peak_hour_rate": turf.peak_hour_rate,
                    "discount": turf.discount,
                    "owner_name": turf.owner_name,
                    "turf_contact_phone": turf.turf_contact_phone,
                    "turf_contact_email": turf.turf_contact_email,
                    "images": turf.images
                    # "image1": turf.image1.url if turf.image1 else None,  # Use image URL if available
                    # "image2": turf.image2.url if turf.image2 else None,
                    # "image3": turf.image3.url if turf.image3 else None,
                    # "image4": turf.image4.url if turf.image4 else None,
                    # "image5": turf.image5.url if turf.image5 else None                
                }
                nearby_turfs.append(turf_data)

        if nearby_turfs:
            return JsonResponse(nearby_turfs, safe=False)
        else:
            return JsonResponse({"message": "No turfs found within 5 km."}, status=404)

@csrf_exempt
def turf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Handle file data if present
        images_data = data.pop('images', [])
        files = []
        for image_data in images_data:
            format, imgstr = image_data['data'].split(';base64,')
            ext = format.split('/')[-1]
            file = ContentFile(base64.b64decode(imgstr), name=f"{image_data['name']}.{ext}")
            files.append(file)

        serializer = TurfSerializer(data=data)
        if serializer.is_valid():
            turf_instance = serializer.save()
            # Save files if any
            for file in files:
                turf_instance.images.create(image=file)
            return JsonResponse({"message": "Turf Data added successfully"}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    if request.method == 'GET':
        item= TurfDetails.objects.all()
        serializer = TurfSerializer(item,many=True)
        return JsonResponse(serializer.data,safe=False)