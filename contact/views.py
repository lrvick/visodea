from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from contact.forms import ContactForm
from django.template import RequestContext, Context
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            from_email = '"%s" <%s>' % (cd['name'], cd['email'])
            try:
#                send_mail(subject,message,from_email, ['lance@openinspires.com','mat@openinspires.com','adam@openinspires.com','hassan@openinspires.com', 'tsopor@gmail.com'])
                send_mail(subject,message,from_email, ['lance@lrvick.net','tsopor@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            return HttpResponseRedirect(reverse('thankyou'))
    else:
        form = ContactForm()
    return render_to_response('contact.html',{'form': form}, context_instance=RequestContext(request))

