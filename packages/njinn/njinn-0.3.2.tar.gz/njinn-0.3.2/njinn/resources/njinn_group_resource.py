from ..base import *
from ..models import *
from .mixins import *


class NjinnGroupResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/groups", NjinnGroup, context)

Mapping.register(NjinnGroup, NjinnGroupResource)
