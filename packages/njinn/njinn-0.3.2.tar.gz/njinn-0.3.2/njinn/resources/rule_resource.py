from ..base import *
from ..models import *
from .mixins import *


class RuleResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/scheduling_rules", Rule, context)

    def duplicate(self, **kwargs) -> Rule:
        return self.operation("duplicate", Rule).post(**kwargs)


Mapping.register(Rule, RuleResource)
