from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from portfolio_app.auth_app.models import PortfolioUser
from portfolio_app.web.models import Blog

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass


# @admin.register(UserModel)
# class PortfolioUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser')
#     search_fields = ('username', 'first_name', 'last_name', 'email')
#     list_filter = ('is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     ordering = ('-date_joined',)
#
#
# # Unregister the default UserModelAdmin for PortfolioUser
# admin.site.unregister(User)
#
# # Register the custom admin class for PortfolioUser
# admin.site.register(PortfolioUser, PortfolioUserAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_filter = ['created_at']
    list_display = ['title', 'author', 'created_at']


admin.site.register(Blog, BlogAdmin)

# class Filter(admin.ModelAdmin):
#     list_display = ['id', 'email', 'created_at', 'role']
#     list_filter = ['created_at', 'role']
#
#
# admin.register(Profile, Filter)
