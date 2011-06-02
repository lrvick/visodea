from django.http import HttpResponse
from django.template import loader, Context
from django.http import Http404
from pages.models import Page
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

def page_handler(request, path=None):
    if not path:
    	page = Page.objects.get_root()[0]
    else:
    	page = get_object_or_404(Page, path=path) 
    if not page.template:
        template = "base.html"
    else:
        template = page.template
    return render_to_response(template, {
    	'page': page,
        }, context_instance=RequestContext(request)) 

#def home(request, path=None):
#	template = 'home.html'
#	return render_to_response(template, {
#    	'page': page,
#        'login_form': AuthenticationForm()
#    }, context_instance=RequestContext(request))
