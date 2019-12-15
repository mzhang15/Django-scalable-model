from django.conf import settings
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import sharded_model
from .routers import logical_shard_of, logical_to_physical
import importlib
import time

from .models import Mapping
from .serializers import MappingSerializer
from .utils import MappingDict

class ResetAll(APIView):
    def post(self, request, format=None):
        print(settings.DATABASES.keys())
        # delete mappings
        all_mappings = Mapping.objects.all().delete()
        # re-initialize mapping
        sharded_model.init_mapping()
        customized_models = importlib.import_module(settings.CUSTOMIZED_MODEL_MODULE)
        shardable_models = settings.SHARDABLE_MODELS.split(',')
        # delete all models and populate new models
        for model in shardable_models:
            for db in settings.DATABASES.keys():
                model_to_del = getattr(customized_models, model)
                model_to_del.objects.using(db).all().delete()
            if getattr(model_to_del, 'is_root'):
                for i in ['a', 'b', 'c', 'd', 'e']:
                    for k in range(10):
                        pkey = i + str(k)
                        model_to_save = model_to_del.objects.using('db1').create(pk="primary_id %s" %pkey)
        return Response(status=status.HTTP_202_ACCEPTED)

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
    split_db = Mapping.objects.get(id=shard_mapping_id).target1
    target_db = Mapping.objects.get(id=shard_mapping_id).target2
    print("start migrating from: %s to %s" % (split_db, target_db))
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

    time.sleep(5) # for demo use

    # 3. update mapping: delete original
    m_w = Mapping.objects.get(id=shard_mapping_id)
    mapping_dict = MappingDict(Mapping.objects.all())
    m_r = mapping_dict.get_mapping(m_w.min_shard)

    mid = m_w.min_shard + int((m_w.max_shard - m_w.min_shard) / 2)
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
    new_mapping_dict = MappingDict(Mapping.objects.all())
    for model in shardable_models:
        print('#########')
        model_to_update = getattr(customized_models, model)
        print(model_to_update)
        origin_db_data = model_to_update.objects.using(split_db).all()
        target_db_data = model_to_update.objects.using(target_db).all()
        for db in [origin_db_data, target_db_data]:
            for data in db:
                shard_key = data.shard_key if hasattr(data, 'shard_key') else data.pk
                write_db = logical_to_physical(logical_shard_of(shard_key), 1)
                print("%%%%%%%%%", write_db, split_db)
                deprecated_db = split_db if db == origin_db_data else target_db
                if write_db != deprecated_db:
                    print('@@@@@deleteing', shard_key, 'from ', deprecated_db)
                    #for child class, need to filter by shard_key
                    model_to_update.objects.using(deprecated_db).filter(pk=data.pk).delete()
            

    # compare its new mapping db with current db, if different, delete
