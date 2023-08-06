from typing import Any

from django.http.response import HttpResponse
from rest_framework import mixins

class UpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse: ...

class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse: ...

class ListModelMixin(mixins.ListModelMixin):
    def list(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse: ...

class RetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse: ...
