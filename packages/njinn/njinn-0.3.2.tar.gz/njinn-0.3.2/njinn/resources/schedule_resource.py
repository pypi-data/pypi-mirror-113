from ..base import *
from ..models import *
from .mixins import *


class ScheduleResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/schedules", Schedule, context)

    def duplicate(self, **kwargs) -> Schedule:
        return self.operation("duplicate", Schedule).post(**kwargs)


Mapping.register(Schedule, ScheduleResource)
