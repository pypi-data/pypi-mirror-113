from ..base import *
from ..models import *
from .mixins import *


class TaskExecutionResource(
    GetResourceMixin, BaseResource,
):
    is_sub_resource = True

    def __init__(self, context):
        super().__init__("tasks", TaskExecution, context)

    def cancel(self, **kwargs) -> None:
        return self.operation("cancel").post(**kwargs)

    def log(self, **kwargs) -> str:
        return self.operation("log", result_class=str).get(**kwargs)


Mapping.register(TaskExecution, TaskExecutionResource)
