from rest_framework import serializers
from .models import Mapping

class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        fields = '__all__'