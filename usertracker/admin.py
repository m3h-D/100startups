from django.contrib import admin
from .models import UserTracker, TheStatus, UserContent
# Register your models here.

class UserTrackerAdmin(admin.ModelAdmin):
    ordering = ['-created_date']
    search_fields = ['user__first__phone', 'user__first__first_name', 'user__first__last_name', 'user_ip', 'the_status']
    # autocomplete_fields = ['user']
    list_display = ('get_phone', 'get_name', 'get_user_type', 'the_status', 'status',)
    list_filter = ('user__is_admin',)

    def get_name(self, obj):
        try:
            name = f'{obj.user.first_name} {obj.user.last_name}'
            return " ".join(name)
        except:
            obj.user_ip

    def get_phone(self, obj):
        try:
            return obj.user.phone
        except:
            return obj.user_ip

    def get_user_type(self, obj):
        try:
            if obj.user.is_admin:
                return 'مدیر سیستم'
            return obj.user.user_type
        except:
            return obj.user_ip

admin.site.register(UserTracker, UserTrackerAdmin)
admin.site.register(TheStatus)
admin.site.register(UserContent)
