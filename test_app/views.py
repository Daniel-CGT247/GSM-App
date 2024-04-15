from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserExtend.objects.select_related("user").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__username"]
    serializer_class = UserSerializer


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = YourListSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return YourListPostSerializer
        return YourListSerializer

    def get_queryset(self):
        return (
            YourList.objects.select_related("item", "created_by__user").prefetch_related("operationlistitem_set__elementlistitem_set__elements__timestudy_set")
            .filter(created_by__user=self.request.user)
            .order_by("-last_update")
        )


class JobGroupViewSet(ModelViewSet):
    queryset = JobGroup.objects.prefetch_related("bundle_groups").all()
    serializer_class = JobGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["list_id"] = self.request.query_params.get("listId")
        return context


class OperationLibViewSet(ModelViewSet):
    queryset = OperationLib.objects.select_related("bundle_group").all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["bundle_group_id"]
    serializer_class = OperationLibSerializer
    permission_classes = [IsAuthenticated]


class OperationListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["list_id", "operations__bundle_group_id"]

    def get_queryset(self):
        return (
            OperationListItem.objects.select_related(
                "list__created_by__user", "list__item", "operations__bundle_group"
            )
            .prefetch_related(
                "elementlistitem_set__options",
                "elementlistitem_set__elements__timestudy_set__elements",
            )
            .filter(list__created_by__user=self.request.user)
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
                "listItem__operations",
            )
            .filter(listItem__list__created_by__user=self.request.user)
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


class SpecialMachineViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SpecialMachineInstuction.objects.all()
    filterset_fields = ["job"]
    serializer_class = SpecialMachineInstuctionSerializer


class OverviewViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = YourList.objects.select_related("item", "created_by__user").order_by(
        "-last_update"
    )
    serializer_class = YourListSerializer


class OperationListOverviewViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["list_id", "operations__bundle_group_id"]

    queryset = OperationListItem.objects.select_related(
        "list__created_by__user", "list__item", "operations__bundle_group"
    ).prefetch_related(
        "elementlistitem_set__options",
        "elementlistitem_set__elements__timestudy_set__elements",
    )
    serializer_class = OperationListDetailSerializer


class ElementListOverviewViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["listItem_id"]

    queryset = ElementListItem.objects.select_related(
        "listItem__list__item",
    ).prefetch_related(
        "elements__operation",
        "options",
        "listItem__operations",
    )
    serializer_class = ElementListItemSerializer
