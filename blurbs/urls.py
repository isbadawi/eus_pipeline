from django.conf.urls.defaults import patterns, include, url
from blurbs.views import SubmitBlurbView

urlpatterns = patterns('',
    url(r'^submit/$', SubmitBlurbView.as_view()),
)
