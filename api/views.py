from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from .serializers import UserSreializer
from .serializers import TurfSerializer
from django.http.response import JsonResponse
from .models import UserDetailsTable
from .models import TurfDetails
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from geopy.distance import geodesic
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
        parser = MultiPartParser()
        data = request.POST.copy()
        data.update(request.FILES)  # Combine request.POST and request.FILES

        serializer = TurfSerializer(data=data)        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Turf Data added successfully"}, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)
    if request.method == 'GET':
        item= TurfDetails.objects.all()
        serializer = TurfSerializer(item,many=True)
        return JsonResponse(serializer.data,safe=False)

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
            return JsonResponse({"message": "Invalid location provided."}, status=400)

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
                    "image1": turf.image.url if turf.image1 else None,  # Use image URL if available
                    "image2": turf.image.url if turf.image2 else None,
                    "image3": turf.image.url if turf.image3 else None,
                    "image4": turf.image.url if turf.image4 else None,
                    "image5": turf.image.url if turf.image5 else None                
                }
                nearby_turfs.append(turf_data)

        if nearby_turfs:
            return JsonResponse(nearby_turfs, safe=False)
        else:
            return JsonResponse({"message": "No turfs found within 5 km."}, status=404)
