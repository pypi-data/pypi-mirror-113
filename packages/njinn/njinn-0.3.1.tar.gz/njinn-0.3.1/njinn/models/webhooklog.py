from __future__ import annotations

from ..base import *
from ..models import *
from .mixins import *


class WebhookLog(BaseModel):
    def __init__(
        self,
        id=None,
        created_at=None,
        updated_at=None,
        source_ip=None,
        http_request_method=None,
        data=None,
        log=None,
        webhook=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.source_ip = source_ip
        self.http_request_method = http_request_method
        self.data = data
        self.log = log
        self.webhook = webhook
