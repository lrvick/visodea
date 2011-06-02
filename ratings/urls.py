from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^submit', 'ratings.views.record_vote'),
    (r'^test', 'ratings.views.testview')
    )
