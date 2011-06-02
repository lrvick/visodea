from django.conf.urls.defaults import *
from projects.views import *
from uploads.views import *

urlpatterns = patterns('', 
   url(r'^add/$', add, name='project-add'), 
   url(r'^search/$', search, name='project-search'),
   url(r'^(?P<slug>[-\w]+)/edit/$', edit, name='project-edit'),
   url(r'^(?P<slug>[-\w]+)/delete/$', delete, name='project-delete'),
   url(r'^(?P<slug>[-\w]+)/adduser/$', adduser, name='project-adduser'),
   url(r'^(?P<slug>[-\w]+)/addfile/$', addfile, name='project-addfile'),
   url(r'^(?P<slug>[-\w]+)/addfavorite/$', addfavorite, name='project-addfavorite'),
   url(r'^(?P<slug>[-\w]+)/manageusers/$', manageusers, name='project-manageusers'),
   url(r'^(?P<slug>[-\w]+)/$', detail, name='project-detail'), 
   url(r'^$', index, name='project-index'), 

)

