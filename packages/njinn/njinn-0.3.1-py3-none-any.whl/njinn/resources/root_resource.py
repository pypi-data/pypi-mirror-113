from ..base import *
from ..models import *
from .mixins import *


class RootResource:
    def __init__(self, client: NjinnClient):
        self.client = client

    def operation(self, path: str, result_class: Type = None):
        return Operation(self.client, path, result_class)

    def schedules_preview(self, **kwargs):
        return self.operation("api/v1/schedules/preview").post(**kwargs)

    def scheduling_rules_preview(self, **kwargs):
        return self.operation("api/v1/scheduling_rules/preview").post(**kwargs)

