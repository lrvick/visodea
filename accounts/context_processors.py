from django.contrib.auth.forms import AuthenticationForm 

def login_form(request):
    return {
        'login_form': AuthenticationForm(),
    }
