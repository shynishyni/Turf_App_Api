from rest_framework import serializers
from .models import UserDetailsTable
from .models import TurfDetails
from .models import TurfImage

class UserSreializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsTable
        fields ='__all__'
    
class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDetails
        fields = [
            'turf_name', 'turf_address', 'turf_city', 'turf_state',
            'turf_zip_code', 'turf_latitude', 'turf_longitude', 'turf_type',
            'surface_type', 'size', 'capacity', 'status', 'opening_time', 
            'closing_time', 'closed_days', 'hourly_rate', 'peak_hour_rate', 
            'discount', 'owner_name', 'turf_contact_phone', 'turf_contact_email',
            'images'
        ]

class TurfImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfImage
        fields = ['image']
