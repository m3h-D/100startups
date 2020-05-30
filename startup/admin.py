from django.contrib import admin
from .models import ShetabDahande, StartUp, StartupComments, UserProfile, Referee, Requests, TeamMember, Investors
# Register your models here.
class StartUpAdmin(admin.ModelAdmin):
    """this will customize the admin panel for StartUp model
       - list_display: what fields to show in list page of StartUp in admin panel
       - list_filter: filter the startups by 3 fields
       - search_fields: search startups by phone number of startup owner, title of startup, id and email of startups owner

    Arguments:
        admin {MODULE} -- a django built-in module to customize admins panel

    """    
    list_display = ('title', 'get_name', 'owner', 'status', 'rahbar', 'rahbar_asli', 'id')
    list_filter = ('is_leader','is_presence_referee', 'is_not_presence_referee')

    search_fields = ('owner__phone', 'title', 'id', 'owner__email')

    def get_name(self, obj):
        """join the owner first name and last name to show it in one of the columns

        Arguments:
            obj {OBJECT} -- object means every startup in the list

        Returns:
            STIRNG -- returns an string with owner first name and last name
        """        
        name = f'{obj.owner.first_name} {obj.owner.last_name}'
        return " ".join(name)

admin.site.register(ShetabDahande)
admin.site.register(StartUp, StartUpAdmin)
admin.site.register(StartupComments)
admin.site.register(UserProfile)
admin.site.register(Referee)
admin.site.register(Requests)
admin.site.register(TeamMember)
admin.site.register(Investors)