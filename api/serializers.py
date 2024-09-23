from rest_framework import serializers
from .models import UserDetailsTable
from .models import TurfDetails

class UserSreializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsTable
        fields ='__all__'
    
class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDetails
        fields ='__all__'
