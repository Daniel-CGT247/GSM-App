from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=ElementListItem)
@receiver(post_delete, sender=ElementListItem)
def update_your_list_last_update(sender, instance, **kwargs):
    instance.listItem.list.last_update = instance.listItem.last_update
    instance.listItem.list.save()


@receiver(post_save, sender=OperationListItem)
@receiver(post_delete, sender=OperationListItem)
def update_your_list_last_update(sender, instance, **kwargs):
    instance.list.last_update = instance.last_update
    instance.list.save()


@receiver(post_save, sender=YourList)
def create_job_group(sender, instance, created, **kwargs):
    if created:
        JobStatus.objects.bulk_create(
            [
                JobStatus(list=instance, name="Bulk", status="Not started"),
                JobStatus(list=instance, name="Bundling", status="Not started"),
                JobStatus(list=instance, name="Sewing", status="Not started"),
                JobStatus(list=instance, name="Donw-Filling", status="Not started"),
                JobStatus(list=instance, name="Finishing", status="Not started"),
            ]
        )
