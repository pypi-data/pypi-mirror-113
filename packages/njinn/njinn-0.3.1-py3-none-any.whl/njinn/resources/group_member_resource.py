from ..base import *
from ..models import *
from .mixins import *


class GroupMemberResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    is_sub_resource = True

    def __init__(self, context):
        super().__init__("members", GroupMember, context)


Mapping.register(GroupMember, GroupMemberResource)
