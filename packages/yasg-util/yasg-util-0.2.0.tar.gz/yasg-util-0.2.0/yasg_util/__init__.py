from enum import Enum
from typing import (
    Callable,
    get_type_hints,
    Optional,
    Dict,
    Any,
    Union,
    Type,
    Tuple,
    List,
)
from functools import wraps

from django.http.response import HttpResponseBase
from drf_yasg.inspectors import (
    SwaggerAutoSchema,
    FieldInspector,
    FilterInspector,
    PaginatorInspector,
)
from drf_yasg.openapi import Schema, SchemaRef, Parameter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from drf_yasg.utils import unset, swagger_auto_schema

__version__ = "0.2.0"


class Location(Enum):
    QUERY = "query"
    BODY = "body"


def get_location(serializer: Union[Type[Serializer], Serializer]) -> Location:
    metaclass = getattr(serializer, "Meta", None)
    if metaclass is None:
        return Location.BODY
    return getattr(metaclass, "location", Location.BODY)


def restapi(
    method: str = None,
    methods: List[str] = None,
    auto_schema: Union[SwaggerAutoSchema, Type[unset]] = unset,
    request_body: Union[Schema, SchemaRef, Serializer, type] = None,
    query_serializer: Serializer = None,
    manual_parameters: List[Parameter] = None,
    operation_id: str = None,
    operation_description: str = None,
    operation_summary: str = None,
    security: List[dict] = None,
    deprecated: bool = None,
    responses: Dict[
        Union[int, str], Union[Schema, SchemaRef, Response, str, Serializer]
    ] = None,
    field_inspectors: List[Type[FieldInspector]] = None,
    filter_inspectors: List[Type[FilterInspector]] = None,
    paginator_inspectors: List[Type[PaginatorInspector]] = None,
    tags: List[str] = None,
    response_model: Optional[Type[Serializer]] = None,
    response_valid: bool = True,
    **extra_overrides: Any
):
    """Decorate a view method to customize the :class:`.Operation` object generated from it.
    from django.urls import path, re_path
    from drf_yasg import openapi
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from rest_framework.fields import IntegerField, CharField, DictField
    from rest_framework.serializers import Serializer
    from rest_framework.views import APIView
    from yasg_util import restapi, Location

    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version='v1',
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )


    class DemoSerializer(Serializer):
        name = CharField(required=True, min_length=2, max_length=20, help_text='姓名')
        age = IntegerField(required=True, min_value=0, max_value=150, help_text='年龄')

        class Meta:
            location = Location.BODY


    class ResponseSerializer(Serializer):
        code = IntegerField(default=200, help_text='状态码')
        msg = CharField(default='success', help_text='响应消息')
        data = DictField(help_text='响应数据')


    class DemoAPIView(APIView):
        @restapi(response_model=ResponseSerializer)
        def post(self, request, pk: int, serializer: DemoSerializer):
            return {'code': 0, 'msg': 'success', 'data': {"pk": pk, "info": serializer.data}}


    urlpatterns = [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('demo/<int:pk>', DemoAPIView.as_view()),
    ]

    """

    def decorator(func: Callable):
        hints = get_type_hints(func)

        _query_serializer = query_serializer
        _request_body = request_body
        _responses = responses or {}
        serializer_cls_dict: Dict[str, Tuple[Location, Type[Serializer]]] = {}

        if response_model and issubclass(response_model, Serializer):
            _responses[200] = response_model()

        for key, value in hints.items():
            if issubclass(value, Serializer):
                location = get_location(value)
                serializer = value()
                assert isinstance(location, Location), "invalid location"
                if location == Location.QUERY:
                    _query_serializer = serializer
                    serializer_cls_dict[key] = (Location.QUERY, value)
                else:
                    _request_body = serializer
                    serializer_cls_dict[key] = (Location.BODY, value)

        @wraps(func)
        def inner(self, request: Request, *args, **kwargs):
            for k, val in serializer_cls_dict.items():
                loc, ser_lcs = val
                data = request.data if loc == Location.BODY else request.query_params
                ser = ser_lcs(data=data)
                ser.is_valid(raise_exception=True)
                kwargs[k] = ser
            result = func(self, request, *args, **kwargs)
            if isinstance(result, HttpResponseBase):
                return result
            if isinstance(result, dict):
                if response_model and response_valid:
                    resp = response_model(data=result)
                    resp.is_valid(raise_exception=True)
                    result = resp.data
                return Response(result)
            return result

        return swagger_auto_schema(
            method,
            methods,
            auto_schema,
            _request_body,
            _query_serializer,
            manual_parameters,
            operation_id,
            operation_description,
            operation_summary,
            security,
            deprecated,
            _responses,
            field_inspectors,
            filter_inspectors,
            paginator_inspectors,
            tags,
            **extra_overrides
        )(inner)

    return decorator
