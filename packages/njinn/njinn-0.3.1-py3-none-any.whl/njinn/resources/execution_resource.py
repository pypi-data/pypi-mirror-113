from ..base import *
from ..models import *
from .mixins import *


class ExecutionResource(GetResourceMixin, SaveResourceMixin, BaseResource):
    def __init__(self, context):
        super().__init__("api/v1/executions", Execution, context)

    def cancel(self, **kwargs) -> None:
        return self.operation("cancel").post(**kwargs)

    def pause(self, **kwargs) -> None:
        return self.operation("pause").post(**kwargs)

    def resume(self, **kwargs) -> None:
        return self.operation("resume").post(**kwargs)
    
    def log(self, **kwargs) -> str:
        return self.operation("log", result_class=str).get(**kwargs)


Mapping.register(Execution, ExecutionResource)
