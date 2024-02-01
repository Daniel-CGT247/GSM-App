from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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
    def get_queryset(self):
        bundle_group = self.request.query_params.get("bundle_group")

        if bundle_group:
            return OperationLib.objects.select_related("bundle_group").filter(
                bundle_group=bundle_group
            )
        return OperationLib.objects.select_related("bundle_group").all()

    serializer_class = OperationLibSerializer


class OperationListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        bundle_group = self.request.query_params.get("bundle_group")
        listId = self.request.query_params.get("listId")

        if bundle_group and listId:
            return (
                OperationListItem.objects.select_related("list__created_by")
                .select_related("operations__bundle_group")
                .prefetch_related("elementlistitem_set__options")
                .prefetch_related(
                    "elementlistitem_set__elements__timestudy_set__elements"
                )
                .filter(
                    list__created_by=self.request.user,
                    operations__bundle_group=bundle_group,
                )
            )

        return (
            OperationListItem.objects.select_related("list__created_by")
            .select_related("operations__bundle_group")
            .prefetch_related("elementlistitem_set__options")
            .prefetch_related("elementlistitem_set__elements__timestudy_set__elements")
            .filter(list__created_by=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method in ["POST", "DELETE"]:
            return OperationListItemSerializer
        return OperationListDetailSerializer


class ElementLibViewSet(ModelViewSet):
    def get_queryset(self):
        operationId = self.request.query_params.get("operation_id")
        if operationId:
            return (
                ElementLib.objects.select_related("operation__bundle_group")
                .prefetch_related("variables__options")
                .filter(operation=operationId)
            )
        return (
            ElementLib.objects.select_related("operation__bundle_group")
            .prefetch_related("variables__options")
            .all()
        )

    serializer_class = ElementLibSerializer


class ElementListItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        operationList = self.request.query_params.get("operationList")

        if operationList:
            return (
                ElementListItem.objects.select_related(
                    "listItem__list__item",
                    "listItem__operations",
                    "elements__operation",
                )
                .prefetch_related("options")
                .prefetch_related("elements__timestudy_set")
                .filter(listItem=operationList)
            )

        return (
            ElementListItem.objects.select_related(
                "listItem__list__item", "listItem__operations", "elements__operation"
            )
            .prefetch_related("options")
            .prefetch_related("elements__timestudy_set")
            .filter(listItem__list__created_by=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return AddElementListItemSerializer
        return ElementListItemSerializer


class TimeStudyViewSet(ModelViewSet):
    queryset = (
        TimeStudy.objects.select_related("elements")
        .prefetch_related("options")
        .select_related("elements__operation__bundle_group")
        .all()
    )
    serializer_class = TimeStudySerializer
