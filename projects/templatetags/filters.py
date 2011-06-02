from django.template.defaultfilters import stringfilter
from django import template
import re
import os
import locale

register = template.Library()

@register.filter
@stringfilter
def youtube(url):
     regex = re.compile(r'http://www.youtube.com/watch\?v=([A-Za-z0-9-=_]+)')
     match = regex.match(url)
     if not match: return ""
     video_id = match.groups()[0]
     return """
      <object width="640" height="385">
        <param name="movie" value="http://www.youtube.com/watch/v/%s"></param>
        <param name="allowFullScreen" value="true"></param>
        <embed src="http://www.youtube.com/watch/v/%s" type="application/x-shockwave-flash" allowfullscreen="true" width="640" height="386"></embed>
      </object>
      """ % (video_id, video_id)
youtube.is_safe = True

@register.filter(name='percentage')  
def percentage(fraction, population):  
    try:  
        return "%i" % ((float(fraction) / float(population)) * 100)  
    except ValueError:  
        return ''


@register.filter(name='ext')
@stringfilter #expects string
def file_ext(filename):
    try:
        name, ext = os.path.splitext(filename)
        return ext[1:]
    except ValueError:
        return {}


@register.filter()
def currency(value):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    return locale.currency(value, grouping=True)

