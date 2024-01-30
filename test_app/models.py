from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
from django.core.exceptions import ValidationError
import re


def isItemNameValid(itemName):
    pattern = r"^\d{4}[a-zA-Z]{1,7}$"
    if not re.match(pattern, itemName):
        raise ValidationError(
            "The item name must start with 4 digits and followed by 1-7 characters"
        )


def isSeasonValid(season):
    pattern = r"^(SP|FW)\d{4}$"
    if not re.match(pattern, season):
        raise ValidationError("Season must start with SP/FW followed by year (YYYY)")


class JobGroup(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="media/")
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BundleGroup(models.Model):
    name = models.CharField(max_length=200, null=True)
    job_group = models.ForeignKey(
        JobGroup, on_delete=models.PROTECT, related_name="bundle_groups"
    )

    def __str__(self):
        return self.name


class NewItem(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        validators=[isItemNameValid],
        verbose_name="Item Number",
    )
    description = models.CharField(max_length=250, null=True)
    season = models.CharField(max_length=250, null=True, validators=[isSeasonValid])
    proto = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="base/media/newItems", null=True, blank=True)

    def __str__(self):
        return self.name


class YourList(models.Model):
    item = models.OneToOneField(NewItem, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name}"


class Option(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name}"


class Variables(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    options = models.ManyToManyField(Option, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RefStyle(models.Model):
    name = models.CharField(max_length=200, unique=True)
    attribute = models.ManyToManyField(Option)

    def __str__(self):
        return self.name


class OperationLib(models.Model):
    bundle_group = models.ForeignKey(BundleGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    operation_code = models.IntegerField()
    note = models.TextField(max_length=1500, null=True, blank=True)
    refStyle = models.ManyToManyField(
        RefStyle,
        blank=True,
        verbose_name="Ref Style",
    )

    def __str__(self):
        return f"{self.name}"


class OperationListItem(models.Model):
    list = models.ForeignKey(YourList, on_delete=models.PROTECT)
    operations = models.ForeignKey(OperationLib, on_delete=models.PROTECT)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.list.item.name}"


class ElementLib(models.Model):
    name = models.CharField(max_length=500, null=True)
    operation = models.ForeignKey(OperationLib, on_delete=models.PROTECT)
    note = models.TextField(max_length=1500, null=True, blank=True)
    variables = models.ManyToManyField(Variables, blank=True)
    my_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["my_order"]

    def __str__(self):
        return f"{self.name}"


class ElementListItem(models.Model):
    listItem = models.ForeignKey(OperationListItem, on_delete=models.PROTECT)
    elements = models.ForeignKey(ElementLib, on_delete=models.CASCADE)
    expanding_name = models.CharField(max_length=500, null=True, blank=True)
    options = models.ManyToManyField(Option, blank=True)
    nmt = models.FloatField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listItem.list.item.name} - {self.elements.name}"


class TimeStudyRef(models.Model):
    elements = models.ForeignKey(ElementLib, on_delete=models.PROTECT)
    refStyle = models.ForeignKey(RefStyle, on_delete=models.PROTECT)
    time = models.FloatField(null=True)


class TimeStudy(models.Model):
    elements = models.ForeignKey(ElementLib, on_delete=models.CASCADE)
    options = models.ManyToManyField(Option, blank=True)
    time = models.FloatField()

    def __str__(self):
        return f"{self.elements.name}"
