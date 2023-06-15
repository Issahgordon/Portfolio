from rest_framework import serializers
from . models import SignUp_info


class Manager_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp_info
        fields = '__all__'