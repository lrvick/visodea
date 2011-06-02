from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
import datetime

class Attachment(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    file = models.FileField(upload_to='attachments') 
    project = models.ForeignKey(Project, blank=True)
    def __unicode__(self):
        return self.name
