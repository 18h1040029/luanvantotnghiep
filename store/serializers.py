from rest_framework.serializers import ModelSerializer
from .models import *


class storeSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields= ["name"]