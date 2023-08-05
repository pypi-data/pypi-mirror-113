from __future__ import annotations

import functools
import inspect
import typing
from copy import deepcopy
from typing import List, Type, TypeVar, Union

from njinn import utils

from .njinn_client import ContentType, NjinnClient

T = TypeVar("T")


class BaseResource:
    is_sub_resource = False

    def __init__(
        self, path: str, model_class: Type, context: Union[NjinnClient, BaseResource]
    ):
        self._path = path
        self.model_class = model_class

        if self.is_sub_resource:
            self.parent: BaseResource = context
            self.client: NjinnClient = context.client
        else:
            self.parent = None
            self.client = context

        self.identifier = None

    @property
    def path(self) -> str:
        def with_identifier():
            return f"/{self.identifier}" if self.identifier else ""

        parent = getattr(self, "parent", None)
        if parent:
            return f"{parent.path}/{self._path}{with_identifier()}"
        return f"{self._path}{with_identifier()}"

    @classmethod
    def construct_model(cls, context, response: dict):
        return cls(context).construct(response)

    def construct(self, response: dict):
        for attr, clazz in Mapping.get_reference_attributes(self.model_class):
            value = response.get(attr, None)
            if type(value) is dict:
                response[attr] = Mapping.lookup_resource(clazz).construct_model(
                    self, value
                )

        return self.model_class(api_resource=self, **response)

    def operation(self, path: str, result_class: Type = None):
        return Operation(self.client, f"{self.path}/{path}", result_class)


def model_init(func):
    """
    Swap kwargs based on _property_map to avoid aguments containing special characters like hyphen
    """

    @functools.wraps(func)
    def __init__(self, *args, **kwargs):
        for prop, attr in self._property_map.items():
            if attr in kwargs:
                kwargs.setdefault(prop, kwargs.pop(attr))

        # Call original __init__
        func(self, *args, **kwargs)

    return __init__


class BaseModel:
    _internal = ["_api_resource", "_read_only", "_submodels", "_property_map"]
    _read_only = []
    _submodels = []
    _property_map = {}

    def __new__(cls, *args, **kwargs):
        """
        Declare properties and backing attributes based on _property_map
        """
        for prop, attr in cls._property_map.items():
            setattr(cls, attr, None)
            setattr(
                cls,
                prop,
                property(
                    fget=lambda obj, key=attr: getattr(obj, key),
                    fset=lambda obj, value, key=attr: setattr(obj, key, value),
                ),
            )

        # Decorate __init__ to treat special arguments
        cls.__init__ = model_init(cls.__init__)
        return object.__new__(cls)

    def __init__(self, api_resource: BaseResource = None):
        self._api_resource = api_resource

    @property
    def api_identifier(self):
        return getattr(self, "id", None)

    @property
    def api_resource(self) -> BaseResource:
        if self._api_resource is None:
            if self.api_identifier is None:
                raise Exception(
                    f"{self} does not have '_api_resource'. Object needs to be created by NjinnAPI or parent resource first."
                )
            raise Exception(f"{self} does not have '_api_resource'")

        def renew_api_resource():
            if self._api_resource.identifier != self.api_identifier:
                self._api_resource = deepcopy(self._api_resource)
                self._api_resource.identifier = self.api_identifier
            return self._api_resource

        return renew_api_resource()

    def refresh(self: T) -> T:
        return self._refresh(self.api_resource.get(self.api_identifier))

    def _refresh(self: T, instance: T) -> T:
        for attr in self.__dict__:
            if hasattr(instance, attr):
                self.__setattr__(attr, deepcopy(getattr(instance, attr)))

        return self


class Mapping:
    _resource_map = {}

    @staticmethod
    def register(model_class: Type, resource_class):
        Mapping._resource_map[model_class] = resource_class

    @staticmethod
    def lookup_resource(model_class: Type) -> Type:
        if model_class in Mapping._resource_map.keys():
            return Mapping._resource_map[model_class]

        raise NotImplementedError(f"{model_class} has no backing resource")

    @staticmethod
    @functools.lru_cache()
    def get_model_classes() -> dict:
        return {
            model_class.__name__: model_class
            for model_class in Mapping._resource_map.keys()
        }

    @staticmethod
    @functools.lru_cache()
    def get_reference_attributes(model_class):
        refs = []
        for attr, type_hint in typing.get_type_hints(
            model_class.__init__, localns=Mapping.get_model_classes()
        ).items():
            clazz = utils.try_get_annotation_class(
                type_hint, lambda t: issubclass(t, BaseModel)
            )
            if clazz is not None:
                refs.append((attr, clazz))

        return refs


class ResourceUtil:
    def __init__(
        self,
        resource_class: Type[BaseResource],
        context: Union[NjinnClient, BaseResource],
    ):
        self.resource_class = resource_class
        self.context = context

    def get(self, identifier=None, **kwargs) -> Union[BaseModel, List[BaseModel]]:

        resource = self.resource_class(self.context)
        return resource.get(identifier, **kwargs)

    def create(self, obj: BaseModel) -> BaseModel:
        resource = self.resource_class(self.context)
        return resource.create(obj)

    @classmethod
    def to_json(cls, obj: dict, exclude_none=False, fields: List = None):
        copy = obj.copy() if type(obj) is dict else obj.__dict__.copy()

        is_base_model = issubclass(type(obj), BaseModel)
        excluded_fields = (obj._read_only + obj._internal) if is_base_model else []

        json = {}
        for key in copy:
            if fields and key not in fields:
                continue

            if key in excluded_fields:
                continue

            value = copy[key]
            if exclude_none and value is None:
                continue

            if type(value) is dict or hasattr(value, "__dict__"):
                json[key] = ResourceUtil.to_json(value, exclude_none=exclude_none)
            else:
                json[key] = value

        return json


class Operation:
    def __init__(
        self, client: NjinnClient, path: str, result_class: Type = None,
    ):
        self.client = client
        self.path = path
        self.result_class = result_class

    def post(self, **kwargs):
        body = ResourceUtil.to_json(kwargs, exclude_none=True)
        response = self.client.post(self.path, body)
        return self.construct(response)

    def get(self, **kwargs):
        if self.result_class is str:
            response = self.client.get(
                self.path, response_content_type=ContentType.TEXT, params=kwargs
            )
        else:
            response = self.client.get(self.path, params=kwargs)
        return self.construct(response)

    def construct(self, response):
        if self.result_class is None or self.result_class is str:
            return response

        if issubclass(self.result_class, BaseModel):
            resource_class = Mapping.lookup_resource(self.result_class)
            return resource_class(self.client).construct(response)

        return self.result_class(**response)


def operation(func):
    """
    Forward the method call from model to corresponding method of the backing resource
    """

    @functools.wraps(func)
    def resource_operation(*args, **kwargs):
        args_name = list(inspect.signature(func).parameters.keys())
        args_dict = dict(zip(args_name[1:], args[1:]))
        kwargs.update(args_dict)

        operation = getattr(args[0].api_resource, func.__name__)
        return operation(**kwargs)

    return resource_operation
