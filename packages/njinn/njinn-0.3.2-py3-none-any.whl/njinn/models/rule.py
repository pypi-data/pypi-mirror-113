from __future__ import annotations

from ..base import *
from .mixins import *


class Rule(SaveModelMixin, DeleteModelMixin, BaseModel):
    def __init__(
        self,
        id=None,
        name=None,
        created_at=None,
        updated_at=None,
        updated_by=None,
        version=None,
        title=None,
        rule_type=None,
        rrule=None,
        grouping_rule=None,
        fixed_offset_rule=None,
        relative_offset_rule=None,
        project=None,
        business_calendar=None,
        labels=None,
        description=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.name = name
        self.version = version
        self.title = title
        self.rule_type = rule_type
        self.rrule = rrule
        self.grouping_rule = grouping_rule
        self.fixed_offset_rule = fixed_offset_rule
        self.relative_offset_rule = relative_offset_rule
        self.project = project
        self.business_calendar = business_calendar
        self.labels = labels
        self.description = description

    _read_only = [
        "id",
        "version",
        "updated_by",
        "updated_at",
        "created_at",
    ]

    @operation
    def duplicate(self, name=None, title=None) -> Rule:
        pass
