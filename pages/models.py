from django.db import models
from django.contrib.admin.models import User
from tagging.fields import TagField
from datetime import datetime
from markitup.fields import MarkupField

class PageManager(models.Manager):
	def get_root(self):
		root = self.get_query_set().filter(path='')
		return root

class Page(models.Model):
    title = models.CharField('Title', max_length=255)
    path = models.SlugField('Path', max_length=255, unique=True, blank=True)
    date = models.DateTimeField('Published on', default=datetime.now)
    description = models.CharField('Description', max_length=255, blank=True)
    body = MarkupField()
    tags = TagField(blank=True)
    objects = PageManager()
    draft = models.BooleanField('Safe as draft',default=False)
    template = models.CharField(max_length=250,blank=True)
    def __unicode__(self):
        return self.title

