
from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import importlib

from .models import Mapping
from .serializers import MappingSerializer

class MappingList(APIView):
    """
    List all mappings, or create a new mapping.
    """
    def get(self, request, format=None):
        mappings = Mapping.objects.all()
        serializer = MappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MappingDetail(APIView):
    """
    Retrieve, update or delete a mapping instance.
    """
    def get_object(self, pk):
        try:
            return Mapping.objects.get(pk=pk)
        except Mapping.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mapping = self.get_object(pk)
        serializer = MappingSerializer(mapping)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print("update mapping: ", pk)
        mapping = self.get_object(pk)
        serializer = MappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # start migration
            migration(pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def migration(shard_mapping_id):
    print("start migrating: ", )
    split_db = Mapping.objects.get(id = shard_mapping_id)
    customized_models = importlib.import_module(settings.CUSTOMIZED_MODEL_MODULE)
    shardable_models = settings.SHARDABLE_MODELS.split(',')
    for model in shardable_models:
        model_to_migrate = getattr(customized_models, model)
        print(model_to_migrate)
        model_to_migrate.objects.using(split_db).all() 