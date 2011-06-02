from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from pages.views import page_handler

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^account/', include('accounts.urls')),
	(r'^projects/', include('projects.urls')),
	(r'^contact/', include('contact.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ratings/', include('ratings.urls')),
	url(r'(.*)/$|^$', page_handler, name="page"),
)

