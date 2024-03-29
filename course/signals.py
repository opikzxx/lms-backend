from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Course, CourseDetail

# Course Model
@receiver(post_delete, sender=Course)
def delete_file_on_model_delete_course(sender, instance, **kwargs):
    if instance.image_url:
        file_path = instance.image_url.name
        default_storage.delete(file_path)

@receiver(pre_save, sender=Course)
def delete_file_on_change_course(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_file_path = old_instance.image_url.name
            new_file_path = instance.image_url.name

            if old_file_path != new_file_path:
                default_storage.delete(old_file_path)
        except sender.DoesNotExist:
            pass