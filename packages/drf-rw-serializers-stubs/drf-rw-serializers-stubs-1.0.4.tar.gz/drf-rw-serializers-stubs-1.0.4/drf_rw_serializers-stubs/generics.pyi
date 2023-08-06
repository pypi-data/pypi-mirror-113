from typing import Any, Type

from django.http.response import HttpResponse
from rest_framework import generics, mixins
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from .mixins import (CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                     UpdateModelMixin)

class GenericAPIView(generics.GenericAPIView):
    def get_serializer_class(self) -> Type[BaseSerializer]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        ...
    def get_read_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        """
        Return the serializer instance that should be used for serializing output.
        """
        ...
    def get_read_serializer_class(self) -> Type[BaseSerializer]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.read_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        ...
    def get_write_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        """
        Return the serializer instance that should be used for validating
        and deserializing input.
        """
        ...
    def get_write_serializer_class(self) -> Type[BaseSerializer]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.write_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins can send extra fields, others cannot)
        """
        ...

class CreateAPIView(CreateModelMixin, GenericAPIView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class UpdateAPIView(UpdateModelMixin, GenericAPIView):
    def put(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class ListAPIView(ListModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class RetrieveAPIView(RetrieveModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class ListCreateAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def post(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class RetrieveDestroyAPIView(
    RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class RetrieveUpdateAPIView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...

class RetrieveUpdateDestroyAPIView(
    RetrieveModelMixin, UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse: ...
