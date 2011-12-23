from django.conf.urls.defaults import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eus_blurbs.views.home', name='home'),
    # url(r'^eus_blurbs/', include('eus_blurbs.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
