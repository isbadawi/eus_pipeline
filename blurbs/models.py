from django.db import models
import tinymce.models
import datetime

class BlurbManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(
            run_until__gte=datetime.date.today()
        )

class Blurb(models.Model):
    title = models.CharField(max_length=50)
    body = tinymce.models.HTMLField()
    comments = tinymce.models.HTMLField(blank=True)
    author = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    run_until = models.DateField()
    approved = models.BooleanField(default=False)

    objects = BlurbManager()

    def __unicode__(self):
        return self.title

    def contact_info(self):
        return '%s <<a href="mailto:%s">%s</a>>' % (
            self.author, self.email, self.email
        )
    contact_info.allow_tags = True
    contact_info.short_description = 'Submitted by'
