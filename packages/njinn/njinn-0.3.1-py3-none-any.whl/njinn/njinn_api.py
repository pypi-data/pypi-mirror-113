from typing import List, Union

from .base import *
from .models import *
from .models.mixins import ParentMixin
from .njinn_client import NjinnClient
from .resources import *


class NjinnAPI(ParentMixin):
    _submodels = [Workflow, Config, Execution, NjinnGroup, Webhook, Schedule, Rule]

    def __init__(
        self, host: str, username: str = None, password: str = None, token: str = None
    ):
        self.client = NjinnClient(
            host, username=username, password=password, token=token
        )
        self.api_resource = RootResource(self.client)

    def workflows(self, identifier=None, **kwargs) -> Union[Workflow, List[Workflow]]:
        return self._get(Workflow, identifier, **kwargs)

    def configs(self, identifier=None, **kwargs) -> Union[Config, List[Config]]:
        return self._get(Config, identifier, **kwargs)

    def executions(
        self, identifier=None, **kwargs
    ) -> Union[Execution, List[Execution]]:
        return self._get(Execution, identifier, **kwargs)

    def groups(self, identifier=None, **kwargs) -> Union[NjinnGroup, List[NjinnGroup]]:
        return self._get(NjinnGroup, identifier, **kwargs)

    def hooks(self, identifier=None, **kwargs) -> Union[Webhook, List[Webhook]]:
        return self._get(Webhook, identifier, **kwargs)

    def schedules(self, identifier=None, **kwargs) -> Union[Schedule, List[Schedule]]:
        return self._get(Schedule, identifier, **kwargs)

    def scheduling_rules(self, identifier=None, **kwargs) -> Union[Rule, List[Rule]]:
        return self._get(Rule, identifier, **kwargs)

    @operation
    def schedules_preview(self, schedule=None) -> dict:
        pass

    @operation
    def scheduling_rules_preview(
        self,
        name=None,
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
        count=None,
    ) -> dict:
        pass
