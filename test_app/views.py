from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username"]
    serializer_class = UserSerializer


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = YourListSerializer

    def get_queryset(self):
        return (
            YourList.objects.select_related("item", "created_by")
            .filter(created_by=self.request.user)
            .order_by("-last_update")
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class JobGroupViewSet(ModelViewSet):
    queryset = JobGroup.objects.prefetch_related("bundle_groups").all()
    serializer_class = JobGroupSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["list_id"] = self.request.query_params.get("listId")
        return context


class OperationLibViewSet(ModelViewSet):
    queryset = OperationLib.objects.select_related("bundle_group").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["bundle_group_id"]
    serializer_class = OperationLibSerializer


class OperationListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["list__item_id", "operations__bundle_group_id"]

    def get_queryset(self):
        return (
            OperationListItem.objects.select_related(
                "list__created_by", "list__item", "operations__bundle_group"
            )
            .prefetch_related(
                "elementlistitem_set__options",
                "elementlistitem_set__elements__timestudy_set__elements",
            )
            .filter(list__created_by=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddOperationItemSerializer
        return OperationListDetailSerializer


class ElementLibViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["operation"]
    serializer_class = ElementLibSerializer
    queryset = ElementLib.objects.prefetch_related(
        "operation__bundle_group", "variables__options"
    ).all()


class ElementListItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["listItem_id"]

    def get_queryset(self):
        return (
            ElementListItem.objects.select_related(
                "listItem__list__item",
            )
            .prefetch_related(
                # "elements__timestudy_set",
                "elements__operation",
                "options",
                # "listItem__operations",
            )
            .filter(listItem__list__created_by=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddElementListItemSerializer
        return ElementListItemSerializer


class TimeStudyViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["elements", "options"]

    queryset = (
        TimeStudy.objects.select_related("elements")
        .prefetch_related("options")
        .prefetch_related("elements__operation__bundle_group")
        .all()
    )
    serializer_class = TimeStudySerializer
