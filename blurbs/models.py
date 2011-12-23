from django.db import models
import tinymce.models

class BlurbManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(
            run_until__gte=datetime.date.today()
        )

class Blurb(models.Model):
    title = models.CharField(max_length=50)
    body = tinymce.models.HTMLField()
    author = models.CharField(max_length=50)
    email = models.EmailField()
    run_until = models.DateField()
    approved = models.BooleanField(default=False)

    objects = BlurbManager()

    def __unicode__(self):
        return self.title

    def active(self):
        return self.run_until >= datetime.date.today()
