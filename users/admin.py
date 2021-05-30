from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from .forms import SignUpForm # CustomUserChangeForm   
from .models import CustomUser, Profile
from django.utils.translation import ugettext_lazy as _

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name', 'is_staff')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'display_name', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('display_name', 'date_of_birth', 'address1', 'address2', 'zip_code', 'city', 'country', 'mobile_phone',)}),
    )
    # (
    #     (None, {'fields': ('email','password',)}),
    # )
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
