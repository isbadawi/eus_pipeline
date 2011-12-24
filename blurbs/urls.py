from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from blurbs.forms import BlurbForm

urlpatterns = patterns('',
    url(r'^submit/$', CreateView.as_view(
        template_name='blurbs/submit.html',
        form_class=BlurbForm,
        success_url='/blurbs/submitted/',
    ), name='submit'),
    url(r'^submitted/$', TemplateView.as_view(
        template_name='blurbs/submitted.html'
    ), name='submitted'), 
)
