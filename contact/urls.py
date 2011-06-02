from contact.views import contact 
from django.conf.urls.defaults import *
from contact.forms import ContactForm
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(r'^thankyou/$', direct_to_template, {'template': 'thankyou.html'}, name="thankyou"),
    url(r'^$', contact),
)


