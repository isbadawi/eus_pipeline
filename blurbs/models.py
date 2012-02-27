from django.db import models
from django.db.models.signals import post_delete
import tinymce.models
import datetime
from blurbs.validators import validate_wordcount
from blurbs.fields import DeletingFileField

class BlurbManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(
            run_until__gte=datetime.date.today(),
            approved=True,
        )

class Blurb(models.Model):
    title = models.CharField(max_length=80)
    body = tinymce.models.HTMLField(validators=[validate_wordcount(250)],
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
    data = DeletingFileField(upload_to='documents')

    def __unicode__(self):
        return self.title

class Email(models.Model):
    label = models.CharField(max_length=50)
    body = tinymce.models.HTMLField(help_text="""
    <p>To incorporate information about the blurb in question, you have
    access to a special variable called {{ blurb }}. In particular, you
    may write:</p>
    <ul>
    <li>{{ blurb.title }} to get the blurb's title</li>
    <li>{{ blurb.body|safe }} to get the text of the blurb</li>
    <li>{{ blurb.run_until }} to get the date until which the blurb will
    run. The default format is "AP-style month dd, yyyy" 
    (e.g. Feb. 14, 2012); this can be adjusted by writing 
    {{ blurb.run_until|date:'format' }} with a special format string, which
    is documented <a href="https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date">here</a>. 
    For instance, a dd/mm/yyyy format corresponds to
    {{ blurb.run_until|date:'d/m/Y' }}. (The default format corresponds to
    {{ blurb.run_until|date:'N j, Y' }}).</li>
    <li>{{ blurb.date_submitted }} to get the date the blurb was submitted
    (the date format comments apply here too).</li>
    <li>{{ blurb.name }} and {{ blurb.email }} to get the submitter's
    contact info. Note that since this is optional, these may be empty.</li>
    </ul>
    <p>If this is a rejection email, you also have access to a variable
    called {{ reason }} which holds a short description of the rejection
    reason (again, potentially empty). You can check for this with
    {% if reason %} --- {% else %} --- {% endif %}.</p>
    """)

    def __unicode__(self):
        return self.label
