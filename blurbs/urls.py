from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from blurbs.views import SubmitBlurbView

urlpatterns = patterns('',
    url(r'^submit/$', SubmitBlurbView.as_view(), name='submit'),
    url(r'^submitted/$', TemplateView.as_view(template_name='blurbs/submitted.html'), name='submitted'), 
)
