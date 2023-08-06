from rest_framework import mixins, viewsets

from .generics import GenericAPIView
from .mixins import (CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                     UpdateModelMixin)

class GenericViewSet(GenericAPIView, viewsets.GenericViewSet): ...
class ModelViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
): ...
class ReadOnlyModelViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet): ...
