from ..base import *
from ..models import *
from .mixins import *


class WebhookLogResource(
    GetResourceMixin, BaseResource,
):
    is_sub_resource = True

    def __init__(self, context):
        super().__init__("log", WebhookLog, context)


Mapping.register(WebhookLog, WebhookLogResource)
