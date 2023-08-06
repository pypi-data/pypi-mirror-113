from ..base import *
from ..models import *
from .mixins import *


class WorkflowResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/workflows", Workflow, context)

    def run(self, **kwargs):
        return self.operation("run", Execution).post(**kwargs)

    def duplicate(self, **kwargs):
        return self.operation("duplicate", Workflow).post(**kwargs)


Mapping.register(Workflow, WorkflowResource)
