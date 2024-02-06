from rest_framework import serializers
from .models import *


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewItem
        fields = ["id", "name", "description", "season", "image", "proto"]


class YourListSerializer(serializers.ModelSerializer):
    item = CollectionSerializer()
    created_by = serializers.StringRelatedField()
    last_update = serializers.SerializerMethodField("get_last_update")

    class Meta:
        model = YourList
        fields = ["id", "item", "complete", "created_by", "last_update"]

    def get_last_update(self, your_list):
        return self.format_timestamp(your_list.last_update)

    def format_timestamp(self, timestamp):
        if timestamp:
            formatted_time = timestamp.strftime("%m/%d/%Y %H:%M:%S")
            return formatted_time
        return None

    def create(self, validated_data):
        item_data = validated_data.pop("item")
        item_instance = NewItem.objects.create(**item_data)
        your_list_instance = YourList.objects.create(
            item=item_instance, **validated_data
        )
        return your_list_instance


class BundleGroupSerializer(serializers.ModelSerializer):
    operations_count = serializers.SerializerMethodField("get_operations_count")

    class Meta:
        model = BundleGroup
        fields = ["id", "name", "operations_count"]

    def get_operations_count(self, bundle_group):
        list_id = self.context.get("list_id")
        if list_id:
            return bundle_group.operationlib_set.filter(
                operationlistitem__list=list_id
            ).count()
        return 0


class JobGroupSerializer(serializers.ModelSerializer):
    bundle_groups = BundleGroupSerializer(many=True)

    class Meta:
        model = JobGroup
        fields = ["id", "name", "is_finished", "bundle_groups"]


# class RefStyleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RefStyle
#         fields = ["id", "name", "attribute"]


class OperationLibSerializer(serializers.ModelSerializer):
    bundle_group = serializers.StringRelatedField()

    class Meta:
        model = OperationLib
        fields = [
            "id",
            "bundle_group",
            "name",
            "note",
        ]


class OperationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCode
        fields = ["id", "name", "operation_code"]


class AddOperationItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    list = serializers.PrimaryKeyRelatedField(queryset=YourList.objects.all())
    operations = serializers.PrimaryKeyRelatedField(queryset=OperationLib.objects.all())

    class Meta:
        model = OperationListItem
        fields = ["id", "list", "operations"]


class UpdateOperationItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    list = serializers.PrimaryKeyRelatedField(queryset=YourList.objects.all())
    operations = serializers.PrimaryKeyRelatedField(queryset=OperationLib.objects.all())
    expanding_field = OperationCode()

    class Meta:
        model = OperationListItem
        fields = ["id", "list", "operations", "expanding_field"]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "name"]


class VariableSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Variables
        fields = ["name", "options"]


class ElementLibSerializer(serializers.ModelSerializer):
    operation = serializers.PrimaryKeyRelatedField(read_only=True)
    variables = VariableSerializer(many=True)

    class Meta:
        model = ElementLib
        fields = ["id", "name", "operation", "variables", "note", "my_order"]


class ElementSimpleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ElementLib
        fields = ["id", "name"]


class ElementListItemSerializer(serializers.ModelSerializer):
    listItem = serializers.StringRelatedField(read_only=True)
    elements = ElementSimpleSerializer()
    options = OptionSerializer(many=True)
    nmt = serializers.SerializerMethodField("get_nmt")

    class Meta:
        model = ElementListItem
        fields = ["id", "listItem", "elements", "expanding_name", "options", "nmt"]

    def get_nmt(self, obj):
        elements = obj.elements
        options = obj.options.all()

        time_study_result = (
            TimeStudy.objects.select_related("elements")
            .prefetch_related("options")
            .filter(elements=elements)
        )

        matching_records = [
            record
            for record in time_study_result
            if set(record.options.all()) == set(options)
        ]

        return (
            (sum(record.time for record in matching_records) / len(matching_records))
            if matching_records
            else None
        )


class AddElementListItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    listItem = serializers.PrimaryKeyRelatedField(
        queryset=OperationListItem.objects.all()
    )
    elements = serializers.PrimaryKeyRelatedField(queryset=ElementLib.objects.all())
    options = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(), many=True
    )

    class Meta:
        model = ElementListItem
        fields = ["id", "listItem", "elements", "expanding_name", "options"]

    def create(self, validated_data):
        options = validated_data.pop("options")
        element_list_item = ElementListItem.objects.create(**validated_data)
        element_list_item.options.set(options)
        return element_list_item


class OperationListDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    list = serializers.PrimaryKeyRelatedField(queryset=YourList.objects.all())
    operations = OperationLibSerializer()
    expanding_field = OperationCodeSerializer()
    element_count = serializers.SerializerMethodField("get_element_items_count")
    total_sam = serializers.SerializerMethodField("get_total_sam")

    class Meta:
        model = OperationListItem
        fields = [
            "id",
            "list",
            "operations",
            "expanding_field",
            "element_count",
            "total_sam",
            "last_update",
        ]

    def get_element_items_count(self, instance):
        return instance.elementlistitem_set.count()

    def get_total_sam(self, instance):
        nmt_values = [
            ElementListItemSerializer(item).get_nmt(item) or 0
            for item in instance.elementlistitem_set.all()
        ]
        return sum(nmt_values)


class TimeStudySerializer(serializers.ModelSerializer):
    elements = ElementSimpleSerializer()
    options = OptionSerializer(many=True)

    class Meta:
        model = TimeStudy
        fields = ["id", "elements", "options", "time"]
