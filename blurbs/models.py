from django.db import models
import tinymce.models
import datetime
from blurbs.validators import validate_wordcount

class BlurbManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(
            run_until__gte=datetime.date.today(),
            approved=True,
        )

class Blurb(models.Model):
    title = models.CharField(max_length=50)
    body = tinymce.models.HTMLField(validators=[validate_wordcount],
        help_text='At most 250 words. Note that this might be edited.'
    )
    comments = models.TextField(blank=True,
        help_text='If you have any special comments or requests, mention them here. (This will not be included in the pipeline.)'
    )
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    run_until = models.DateField()
    approved = models.BooleanField(default=False)

    objects = BlurbManager()

    class Meta:
        ordering = ['-date_submitted']

    def __unicode__(self):
        return self.title

    def contact_info(self):
        return '%s <<a href="mailto:%s">%s</a>>' % (
            self.name, self.email, self.email
        )
    contact_info.allow_tags = True
    contact_info.short_description = 'Submitted by'

class Document(models.Model):
    blurb = models.ForeignKey(Blurb)
    title = models.CharField(max_length=50)
    data = models.FileField(upload_to='documents')
