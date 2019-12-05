import sys
from django.conf import settings


class DjangoAutoshardSettings:
    def __init__(self):
        try:
            user_settings = settings.DJANGO_AUTOSHARD
        except AttributeError:
            user_settings = {}

        self.__settings = dict(
            NODES=dict(),
            EPOCH='2016-01-01',
            MAX_SHARDS=1 << 13,
        )
        self.__settings.update(user_settings)
        settings.DJANGO_AUTOSHARD = self

    def __getattr__(self, name):
        return self.__settings.get(name)


django_autoshard_settings = DjangoAutoshardSettings()
sys.modules[__name__] = django_autoshard_settings
