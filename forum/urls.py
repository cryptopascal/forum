from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name="home"),    
#    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
#    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root' : settings.STATIC_ROOT}),         
    #media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    #registratin : (uses the default backed from registration app)
    #                some changes are made, we use a customised form to take into consideration additional infos
    #                urls from spec_registration, to use the new form_class
    (r'^accounts/', include('custom_registration.backends.custom.urls')),
    #cities       
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),  
)