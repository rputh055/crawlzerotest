from django.db import models
import os
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# Create your models here.

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join(str(instance.id), filename)

class File(models.Model):
    #owner = models.OneToOneField  (User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)

def __str__(self):
  return self.user.username

@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
@receiver(pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False
    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

