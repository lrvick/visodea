from django.contrib import admin
from projects.models import Project, ProjectMember
from django.db import models

class ProjectMembersInline(admin.TabularInline):
    model = ProjectMember
    extra = 5 

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    inlines = [ProjectMembersInline,]

admin.site.register(Project, ProjectAdmin)

