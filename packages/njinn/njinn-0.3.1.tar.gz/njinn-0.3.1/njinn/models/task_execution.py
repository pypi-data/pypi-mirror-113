from __future__ import annotations

from ..base import *
from .mixins import *


class TaskExecution(BaseModel):
    def __init__(
        self,
        id=None,
        name=None,
        execution=None,
        state=None,
        state_info=None,
        input=None,
        started_at=None,
        ended_at=None,
        runtime=None,
        triggered_by=None,
        position=None,
        active=None,
        result=None,
        queue=None,
        published=None,
        is_error_task=None,
        on_success=None,
        on_complete=None,
        on_error=None,
        action=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.execution = execution
        self.name = name
        self.state = state
        self.state_info = state_info
        self.input = input
        self.started_at = started_at
        self.ended_at = ended_at
        self.runtime = runtime
        self.triggered_by = triggered_by
        self.position = position
        self.active = active
        self.result = result
        self.queue = queue
        self.published = published
        self.is_error_task = is_error_task
        self.action = action
        self.on_success = on_success
        self.on_complete = on_complete
        self.on_error = on_error

    _property_map = {
        "on_success": "on-success",
        "on_complete": "on-complete",
        "on_error": "on-error",
    }

    _read_only = [
        "id",
        "started_at",
        "ended_at",
        "runtime",
        "position",
        "active",
        "queue",
        "published",
        "on-complete",
        "on-error",
        "action",
    ]

    @operation
    def log() -> str:
        pass

    @operation
    def cancel() -> None:
        pass

