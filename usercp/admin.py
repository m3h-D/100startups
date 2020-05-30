from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.admin.sites import AlreadyRegistered
from usercp.models import User, Role
from .forms import UserStartupRegisterForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    """The forms to add and change user instances
    
    Arguments:
        BaseUserAdmin {MODULE} -- a built-in django Admin

    """
    form = UserChangeForm
    add_form = UserStartupRegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'get_name', 'user_type', 'get_roles', 'id')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password', 'username')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'avatar', 'step', 'role', 'category',
                                      'linkdin', 'instagram', 'twitter', 'city', 'site', 'bio', 'birth_date', 'skill', 'grade',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'mentor_user',
                                    'user_type', 'user_type2', 'is_compeleted', 'add_to_mentors', 'can_see', 'can_see_startups', 'sort')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone', 'first_name', 'last_name', 'email', 'id')
    # autocomplete_fields = ['question']
    ordering = ('-id',)
    filter_horizontal = ()

    def get_roles(self, obj):
        """get all roles that assigned to user
        
        Arguments:
            obj {OBJECT} -- all instances of User model
        
        Returns:
            STRING -- reurns am string of roles
        """
        return "\n".join([p.name for p in obj.role.all()])

    def get_name(self, obj):
        """full name of every user
        
        Arguments:
            obj {OBJECT} -- all instances of User Model
        
        Returns:
            STRING -- returns string of first_name and last_name
        """
        name = f'{obj.first_name} {obj.last_name}'
        return " ".join(name)

admin.site.register(User, UserAdmin)
admin.site.register(Role)
