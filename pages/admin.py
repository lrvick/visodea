from django.contrib import admin
from pages.models import Page
from markitup.widgets import AdminMarkItUpWidget
from django.db import models

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'draft')
	search_fields = ('title', 'body', 'tags')
	prepopulated_fields = {"path": ("title",)}

admin.site.register(Page, PageAdmin)

