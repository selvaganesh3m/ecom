from django.contrib import admin
from .models import User, UserAddress


class UserAddressesInline(admin.StackedInline):
    model = UserAddress


class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserAddressesInline,
    ]


admin.site.register(User, UserAdmin)
