from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class UserAdminCustom(UserAdmin):
    list_display = ('name', 'phone_number','city','gender', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'verified')
    search_fields = ('name', 'phone_number', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('name',)
    # add_fieldsets = ('phone_number', 'email')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'gender', 'city', 'profile_pic', 'password1', 'password2')}
        ),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, UserAdminCustom)
