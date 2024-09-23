from rest_framework import serializers
from .models import UserDetailsTable

class UserSreializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsTable
        fields ='__all__'
    