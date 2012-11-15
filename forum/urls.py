import os.path

from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from my_forum.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Browsing
    (r'^$',main_page),
    (r'^add/thread/$',save_thread),
    (r'^thread/(?P<thread_slug>[-\w]+)/$', save_post),      
    
    # Session management
    (r'^login/$','django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$',direct_to_template,
     {'template': 'registration/register_success.html'}
     ),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root' : settings.STATIC_ROOT}),         
    #media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    
    
     
    #registratin : (uses the default backed from registration app)
    #                some changes are made, we use a customised form to take into consideration additional infos
    #                urls from spec_registration, to use the new form_class
    #cities       
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),  
)