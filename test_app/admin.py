from django.contrib import admin
from django.apps import apps
from adminsortable2.admin import SortableAdminMixin
from .models import *
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse

app = apps.get_app_config("test_app")


@admin.register(ElementLib)
class ElementLibAdmin(SortableAdminMixin, admin.ModelAdmin):
    autocomplete_fields = ["variables"]
    ordering = ["my_order"]
    list_display = ["name", "get_variables", "get_operation"]
    search_fields = ["name__istartswith"]
    list_filter = ["operation__name"]
    autocomplete_fields = ["operation", "variables"]

    @admin.display(description="Variables")
    def get_variables(self, element):
        return " | ".join([variable.name for variable in element.variables.all()])

    @admin.display(description="Operation")
    def get_operation(self, element):
        return " | ".join([operation.name for operation in element.operation.all()])


class OperationInline(admin.TabularInline):
    model = OperationLib
    extra = 0
    exclude = ["note", "refStyle"]


@admin.register(BundleGroup)
class BundleGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "job_name"]
    list_select_related = ["job_group"]
    list_per_page = 10
    search_fields = ["name__istartswith"]
    inlines = [OperationInline]

    def job_name(self, obj):
        return obj.job_group.name


class BundleGroupInline(admin.TabularInline):
    model = BundleGroup
    extra = 0


@admin.register(JobGroup)
class JobGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 10
    inlines = [BundleGroupInline]


@admin.register(YourList)
class YourListAdmin(admin.ModelAdmin):
    list_display = ["item", "complete", "created_by", "operations_count", "last_update"]
    list_editable = ["complete"]
    list_per_page = 10
    search_fields = ["item__name__istartswith"]
    list_filter = ["complete", "created_by__username", "last_update"]

    @admin.display(ordering="operations_count")
    def operations_count(self, yourList):
        url = (
            reverse("admin:test_app_operationlistitem_changelist")
            + "?"
            + urlencode({"list_id": str(yourList.id)})
        )
        return format_html(
            "<a href={}>{} operations</a>", url, yourList.operations_count
        )

    @admin.display(description="Operations")
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(operations_count=Count("operationlistitem"))
        )


@admin.register(NewItem)
class NewItemAdmin(admin.ModelAdmin):
    list_display = ["name", "season", "proto", "image"]
    list_editable = ["season", "proto", "image"]
    list_filter = ["season", "proto"]
    search_fields = ["name__istartswith"]
    list_per_page = 10


@admin.register(OperationLib)
class OperationLibAdmin(admin.ModelAdmin):
    list_display = ["name", "job_code", "bundle_group", "elements_count", "note"]
    list_filter = ["bundle_group__name"]
    search_fields = ["name__istartswith"]
    list_per_page = 10
    autocomplete_fields = ["bundle_group"]

    @admin.display(ordering="elements_count")
    def elements_count(self, obj):
        return f"{obj.elementlib_set.count()} elements"


@admin.register(OperationListItem)
class OperationListItemAdmin(admin.ModelAdmin):
    list_display = [
        "list",
        "operations",
        "get_bundle_group",
        "elements_count",
        "get_user",
        "last_update",
    ]
    list_editable = ["operations"]
    list_per_page = 10

    @admin.display(description="created by")
    def get_user(self, operationlistitem):
        return operationlistitem.list.created_by

    @admin.display(description="bundle group")
    def get_bundle_group(self, operationlistitem):
        return operationlistitem.operations.bundle_group

    @admin.display(ordering="operations_count")
    def elements_count(self, list):
        url = (
            reverse("admin:test_app_elementlistitem_changelist")
            + "?"
            + urlencode({"listItem_id": str(list.id)})
        )
        return format_html("<a href={}>{} elements</a>", url, list.elements_count)

    @admin.display(description="elements")
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(elements_count=Count("elementlistitem"))
        )


@admin.register(ElementListItem)
class ElementListItemAdmin(admin.ModelAdmin):
    list_display = ["listItem", "elements", "expanding_name"]
    list_editable = ["elements", "expanding_name"]
    list_filter = [
        "listItem__list__created_by__username",
        "elements__operation__name",
        "last_update",
    ]
    autocomplete_fields = ["options"]
    list_per_page = 10


@admin.register(Variables)
class VariablesAdmin(admin.ModelAdmin):
    list_display = ["name", "get_options"]
    list_per_page = 10
    search_fields = ["name__istartswith"]
    autocomplete_fields = ["options"]

    def get_options(self, variables):
        return " | ".join([option.name for option in variables.options.all()])


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name__istartswith"]
    list_per_page = 10


@admin.register(TimeStudy)
class TimeStudyAdmin(admin.ModelAdmin):
    list_display = ["elements", "time", "get_operation"]
    list_per_page = 10
    search_fields = ["elements__name__istartswith"]
    list_filter = ["elements__operation__name"]
    autocomplete_fields = ["options"]

    @admin.display(description="Operation")
    def get_operation(self, timestudy):
        return timestudy.elements.operation.name


@admin.register(SpecialMachineInstuction)
class SpecialMachineInstuctionAdmin(admin.ModelAdmin):
    list_display = ["job", "image", "created_at", "updated_at"]
    search_fields = ["name__istartswith"]
    list_per_page = 10


try:
    for model_name, model in app.models.items():
        if (
            (model_name == "timestudy_options")
            | (model_name == "elementlistitem_options")
            | (model_name == "elementlib_variables")
            | (model_name == "variables_options")
            | (model_name == "elementlib_operation")
        ):
            admin.site.register(model)
except:
    print("Already registered: ", model_name)
