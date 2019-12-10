
from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import importlib
import time

from .models import Mapping
from .serializers import MappingSerializer
from .utils import MappingDict

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

# TODO: this function should be passed with a callback function
def migration(shard_mapping_id):
    split_db = (Mapping.objects.get(id=shard_mapping_id)).target1
    print("start migrating from: %s to %s" % (split_db, (Mapping.objects.get(id=shard_mapping_id)).target2))
    customized_models = importlib.import_module(settings.CUSTOMIZED_MODEL_MODULE)
    shardable_models = settings.SHARDABLE_MODELS.split(',')

    for model in shardable_models:
        model_to_migrate = getattr(customized_models, model)
        print(model_to_migrate)

        # 1.get related data from original db
        dataset = model_to_migrate.objects.using(split_db).all() 

        # 2. copy data over to dest db
        print("iterate data in db %s" % split_db)
        for data in dataset:
            print(data)
            data.save()

    time.sleep(20) # for demo use

    # 3. update mapping: delete original
    m_w = Mapping.objects.get(id=shard_mapping_id)
    mapping_dict = MappingDict(Mapping.objects.all())
    m_r = mapping_dict.get_mapping(m_w.min_shard)

    mid = int(m_w.max_shard / 2)
    max_shard = m_w.max_shard
    new_db = m_w.target2

    m_r.max_shard = mid
    m_r.save()
    m = Mapping(min_shard=mid+1, max_shard=max_shard, perm=m_r.perm, target1=new_db)
    m.save()

    m_w.max_shard = mid
    m_w.target2 = ''
    m_w.save()
    m = Mapping(min_shard=mid+1, max_shard=max_shard, perm=2, target1=new_db)
    m.save()

    # 4. delete 2nd half data from target1; delete 1st half data from target2
    # for model in shardable_models:
    #     model_to_migrate = getattr(customized_models, model)
    #     print(model_to_migrate)

    #     dataset = model_to_migrate.objects.using(split_db).all() 

    #     for data in dataset:
    #         data.save()