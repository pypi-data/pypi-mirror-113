from __future__ import annotations

from ..base import *
from ..models import *
from .mixins import *


class Execution(ParentMixin, SaveModelMixin, BaseModel):
    def __init__(
        self,
        url=None,
        id=None,
        workflow: Union[int, Workflow] = None,
        labels=None,
        state=None,
        state_info=None,
        input=None,
        params=None,
        started_at=None,
        ended_at=None,
        runtime=None,
        trigger=None,
        webhook: Union[int, Webhook] = None,
        schedule: Union[int, Schedule] = None,
        task=None,
        parent_task_execution=None,
        parent_execution=None,
        result=None,
        user=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.url = url
        self.id = id
        self.workflow = workflow
        self.labels = labels
        self.state = state
        self.state_info = state_info
        self.input = input
        self.params = params
        self.started_at = started_at
        self.ended_at = ended_at
        self.runtime = runtime
        self.trigger = trigger
        self.webhook = webhook
        self.schedule = schedule
        self.task = task
        self.parent_task_execution = parent_task_execution
        self.parent_execution = parent_execution
        self.result = result
        self.user = user

    _read_only = [
        "url",
        "id",
        "runtime",
        "task",
        "parent_task_execution",
        "parent_execution",
    ]

    _submodels = [TaskExecution]

    def tasks(
        self, identifier=None, **kwargs
    ) -> Union[TaskExecution, List[TaskExecution]]:
        return self._get(TaskExecution, identifier, **kwargs)

    @operation
    def cancel(self) -> None:
        pass

    @operation
    def pause(self) -> None:
        pass

    @operation
    def resume(self) -> None:
        pass

    @operation
    def log(self) -> str:
        pass
