from django.db import models
from django.db.models.signals import post_delete

class DeletingFileField(models.FileField):
    "A FileField that deletes the file when the model instance is deleted."
    def contribute_to_class(self, cls, name):
        super(DeletingFileField, self).contribute_to_class(cls, name)
        post_delete.connect(self.delete_file, sender=cls)

    def delete_file(self, instance, sender, **kwargs):
        file = getattr(instance, self.attname)
        if file:
            file.delete(save=False)
