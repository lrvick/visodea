from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from accounts.views import register, profile, profile_edit, account_edit, overview, RegisterWizard, activate
from django.contrib.auth.views import password_change, password_change_done, password_reset, password_reset_confirm, password_reset_done, password_reset_complete
from accounts.forms import UserAccountForm, UserCreationFormExtended, UserProfileForm, UserProfileForm1, UserProfileForm2 
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login,logout
urlpatterns = patterns('',
    url(r'^login/$',  login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^register/$', RegisterWizard([UserCreationFormExtended, UserProfileForm1, UserProfileForm2]), name="register"),
    url(r'^register/success/$', direct_to_template, {'template': 'success.html' }, name="success"), 
    url(r'^overview/$', overview, name="overview"), 
    url(r'^profile/$', profile, name="profile"), 
    url(r'^profile/edit/$', profile_edit, name="profile-edit"),
    url(r'^edit/$', account_edit, name="account-edit"),
    url(r'^password-change/$', password_change),
    url(r'^password-change/done/$', password_change_done),
    url(r'^password-reset/$', password_reset),
    url(r'^password-reset/complete/$', password_reset_complete),
    url(r'^password-reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
    url(r'^password-reset/done/$', password_reset_done),
    url(r'^activate/(?P<verification_key>\w+)/$', activate, name="activate"),
    url(r'^(?P<username>[-\w]+)/$', profile, name="profile"),
    url(r'^$', overview, name="overview"),
)


