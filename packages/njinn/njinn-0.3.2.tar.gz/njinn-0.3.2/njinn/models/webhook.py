from __future__ import annotations

from ..base import *
from ..models import *
from .mixins import *


class Webhook(ParentMixin, SaveModelMixin, DeleteModelMixin, BaseModel):
    def __init__(
        self,
        id=None,
        version=None,
        updated_by=None,
        last_call=None,
        created_at=None,
        updated_at=None,
        labels=None,
        name=None,
        title=None,
        is_active=None,
        key=None,
        source_ip_filter=None,
        header_validation_name=None,
        header_validation_value=None,
        inputs=None,
        description=None,
        workflow: Union[int, Workflow] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.version = version
        self.updated_by = updated_by
        self.last_call = last_call
        self.created_at = created_at
        self.updated_at = updated_at
        self.labels = labels
        self.name = name
        self.title = title
        self.is_active = is_active
        self.key = key
        self.source_ip_filter = source_ip_filter
        self.header_validation_name = header_validation_name
        self.header_validation_value = header_validation_value
        self.inputs = inputs
        self.description = description
        self.workflow = workflow

    _read_only = [
        "id",
        "version",
        "created_at",
        "updated_by",
        "updated_at",
        "last_call",
    ]

    _submodels = [WebhookLog]

    def logs(self, identifier=None, **kwargs) -> Union[WebhookLog, List[WebhookLog]]:
        return self._get(WebhookLog, identifier, **kwargs)

    @operation
    def duplicate(self, name=None, title=None) -> Webhook:
        pass

