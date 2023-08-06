from __future__ import annotations

from ..base import *
from .mixins import *


class Config(SaveModelMixin, DeleteModelMixin, BaseModel):

    def __init__(
        self,
        url=None,
        id=None,
        project=None,
        name=None,
        title=None,
        values=None,
        config_scheme=None,
        labels=None,
        description=None,
        version=None,
        updated_by=None,
        updated_at=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.url = url
        self.id = id
        self.project = project
        self.name = name
        self.title = title
        self.values = values
        self.config_scheme = config_scheme
        self.labels = labels
        self.description = description
        self.version = version
        self.updated_by = updated_by
        self.updated_at = updated_at

    _read_only = [
        "url",
        "id",
        "version",
        "updated_by",
        "updated_at",
        "created_at",
    ]
    
    @operation
    def duplicate(self, name=None, title=None) -> Config:
        pass
