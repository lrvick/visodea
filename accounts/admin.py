
from django.contrib import admin
from accounts.models import UserProfile
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    exclude = ('username','password','groups','user_permissions')
    fk_name = 'user'
    max_num = 1

class CustomUser(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(User, CustomUser)


