from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from blurbs.views import PipelineView, CreateBlurbView

urlpatterns = patterns('',
    url(r'^submit/$', CreateBlurbView.as_view(), name='submit'),
    url(r'^submitted/$', TemplateView.as_view(
        template_name='blurbs/submitted.html'
    ), name='submitted'), 
    url(r'^generate/$', PipelineView.as_view(), name='generate'),
)
