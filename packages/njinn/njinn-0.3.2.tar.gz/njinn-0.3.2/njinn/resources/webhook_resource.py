from ..base import *
from ..models import *
from .mixins import *


class WebhookResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, context):
        super().__init__("api/v1/hooks", Webhook, context)

    def duplicate(self, **kwargs) -> Webhook:
        return self.operation("duplicate", Webhook).post(**kwargs)


Mapping.register(Webhook, WebhookResource)
