from ..base import *
from ..models import *
from .mixins import *


class ConfigResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/configs", Config, context)

    def duplicate(self, **kwargs) -> Config:
        return self.operation("duplicate", Config).post(**kwargs)


Mapping.register(Config, ConfigResource)
