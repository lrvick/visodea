from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from accounts.forms import UserProfileForm, UserAccountForm, UserCreationFormExtended, UserProfileForm1, UserProfileForm2
from django.template import RequestContext
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.core.urlresolvers import reverse
from projects.models import Project
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard import FormWizard
from django.core.mail import send_mail
from django.conf import settings

@login_required
def overview(request):
    user = request.user
    profile = user.get_profile()
    projects = Project.objects.filter(owner=user)
    return render_to_response("overview.html", {
        'user': user,
        'profile': profile,
        'projects': projects,
    }, context_instance=RequestContext(request))

@login_required 
def account_edit(request):
    account = request.user
    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('overview'))
    else:
        form = UserAccountForm(instance=account)
    return render_to_response("account.html", {
        'account_form': form,
    }, context_instance=RequestContext(request))

def profile(request, username=None):
    if username: 
        user = User.objects.get(username=username)
        profile = user.get_profile()
    else:
        user = request.user
        profile = user.get_profile()
    return render_to_response("profile.html", {
        'user': user,
        'profile': profile,
    }, context_instance=RequestContext(request))

@login_required 
def profile_edit(request):
    user = request.user
    profile = user.get_profile()
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[user.username]))
    else:
        form = UserProfileForm(instance=profile)
    return render_to_response("edit.html", {
        'profile_form': form,
    }, context_instance=RequestContext(request))

def register(request):         
    if request.method == 'POST':
        form = UserCreationFormExtended(request.POST,request.FILES)
        if form.is_valid():   
            new_user = form.save()
            new_profile = UserProfile(user=new_user) #create new profile with new_user instance
            new_profile.save()            
            return HttpResponseRedirect(reverse('success'))
    else:                     
        form = UserCreationFormExtended()
    return render_to_response("register.html", locals(), context_instance=RequestContext(request))

class RegisterWizard(FormWizard):
    def done(self, request, form_list):
        for form in form_list:
            if isinstance(form, UserCreationFormExtended):
                user = form.save()
                #set to not active
                user.is_active = 0
                user.save()
            if isinstance(form, UserProfileForm1):
                profile = form.save(commit=False)
                profile.user = user
            if isinstance(form, UserProfileForm2):
                tempprofile = form.save(commit=False)
                for f in form.fields.keys():
                    setattr(profile, f, getattr(tempprofile, f))
                profile.save()
            
        user = User.objects.get(username=user.username)
        message = """Testing for now here's your verifaction URL: http://visodea.com/account/activate/%s """ % (user.get_profile().verification_key) 
        send_mail('Please verify your email', message, 'support@visodea.com', [user.email], fail_silently=False) 
        return HttpResponseRedirect(reverse('success'))
    
    def get_template(self, step):
        return 'register_%s.html' % step

def activate(request, verification_key):
    url_key = verification_key
    profile = get_object_or_404(UserProfile, verification_key=url_key) #404's if key is not found 
    user = profile.user
    user.is_active = 1 #set user to active so they may login
    user.save()
    return render_to_response('email_verified.html', (), context_instance=RequestContext(request))
