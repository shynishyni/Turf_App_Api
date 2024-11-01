from rest_framework import serializers
from .models import UserDetailsTable
from .models import TurfDetails
from .models import TurfBookingDetails

class UserSreializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsTable
        fields ='__all__'
    
class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDetails
        fields='__all__'

class TurfBookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfBookingDetails
        fields = '__all__'  