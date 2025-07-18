# portfolio/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Portfolio, Project
from .forms import PortfolioAdminForm # Import the new form

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['project_name', 'project_description']
    readonly_fields = ['created_at', 'updated_at']

class PortfolioInline(admin.StackedInline):
    model = Portfolio
    can_delete = False
    verbose_name_plural = 'Portfolio'
    fields = ['portfolio_title', 'portfolio_description', 'project']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    # Use the custom form
    form = PortfolioAdminForm

    # The list_display and search_fields can remain largely the same,
    # as the form handles the actual editing.
    list_display = ['__str__', 'portfolio_title', 'display_user_first_name', 'display_user_last_name', 'user_email', 'project']
    list_filter = ['project']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'portfolio_title']

    # Define the fieldsets to control the layout in the admin.
    # This will group the User fields with the Portfolio fields nicely.
    fieldsets = (
        (None, {
            'fields': ('user', 'portfolio_title', 'portfolio_description', 'project'),
        }),
        ('User Personal Information', {
            'fields': ('first_name', 'last_name'),
            'description': 'These fields update the associated User\'s first and last name.',
        }),
    )

    def display_user_first_name(self, obj):
        return obj.user.first_name if obj.user else 'N/A'
    display_user_first_name.short_description = 'First Name'
    display_user_first_name.admin_order_field = 'user__first_name'

    def display_user_last_name(self, obj):
        return obj.user.last_name if obj.user else 'N/A'
    display_user_last_name.short_description = 'Last Name'
    display_user_last_name.admin_order_field = 'user__last_name'

    def user_email(self, obj):
        return obj.user.email if obj.user else 'N/A'
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'


# Re-register UserAdmin (this part remains the same)
class UserAdmin(BaseUserAdmin):
    inlines = (PortfolioInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)