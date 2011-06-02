from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField 
from tagging.fields import TagField
from django.template.defaultfilters import slugify

class Project(models.Model):
    name = models.CharField('Project Name', max_length = 100, unique=True)
    slug = models.SlugField(unique=True)
    company = models.CharField('Corporation', max_length = 100, blank = True)
    date_created = models.DateTimeField(auto_now_add=True)
    founded = models.DateTimeField(auto_now_add=True,blank=True)
    phone = PhoneNumberField(blank=True,)
    email = models.EmailField(max_length=75)
    url = models.URLField(verify_exists=True)
    youtube_intro = models.URLField('Youtube Intro',verify_exists=True, blank=True)
    description = models.TextField('Pitch')
    markets = models.TextField()
    customers = models.TextField('Customers')
    revenue_model = models.TextField('Revenue Model')
    strategy = models.TextField('Sales Strategy')
    tax_id = models.CharField('Tax ID #',max_length=20, blank = True)
    funding_target = models.DecimalField('Current Funding',max_digits = 10, decimal_places=2)
    funding_current = models.DecimalField('Needed Funding',max_digits = 10, decimal_places=2)
    dab_score = models.DecimalField('D&B Score',max_digits = 10,decimal_places=0, blank = True)
    street_line1 = models.CharField('Address 1', max_length = 100, blank = True)
    street_line2 = models.CharField('Address 2', max_length = 100, blank = True)
    city = models.CharField('City', max_length = 100, blank = True)
    state = models.CharField('State', max_length = 100, blank = True)
    zip = models.DecimalField('ZIP', max_digits = 5, decimal_places=0)
    country = models.CharField('Country', max_length = 100, blank = True)
    tags = TagField(blank=True)
    owner = models.ForeignKey(User)    
    is_public = models.BooleanField('List Publically',default=False)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save()         

    def check_member(self, user):
        """Checks the exist of user in a project, if so returns member."""
        members = self.projectmember_set.all()
        if user in [member.user for member in members]:
            return members.get(user=user)

    def __unicode__(self):
        return 'Project - %s' % (self.name,)

class ProjectMember(models.Model):
    LEVELS = (
        ('1', 'Stage 1'),
        ('2', 'Stage 2'),
        ('3', 'Stage 3'),
        ('4', 'Stage 4'),
    )
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    level = models.IntegerField(choices=LEVELS, default=1)
    def __unicode__(self):
        return self.user.username

class ProjectFavorite(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (('project', 'user' )) #this makes it unique at the db level

    def __unicode__(self):
        return self.user.username
