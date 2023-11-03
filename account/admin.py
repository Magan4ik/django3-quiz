from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from account.models import MyUser, Quiz
from account.forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Quiz)

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    model = MyUser
    add_fieldsets = (
    *UserAdmin.add_fieldsets,
        (
        "Custom fields",
            {
                "fields":(
                'avatar',
                )
            }
        )
    )
    fieldsets = (
    *UserAdmin.fieldsets,
        (
        "Custom fields",
            {
                "fields":(
                'avatar',
                )
            }
        )
    )
