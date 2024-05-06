from django.contrib import admin

# Register your models here.
from Profile.models import ProfileModel, UserActivityLog, Notification
# Register your models here.

class ShowProfileModel(admin.ModelAdmin):
    list_display = ('id', 'age', 'sex', 'status')
admin.site.register(ProfileModel, ShowProfileModel)

class ShowUserActivityLog(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity', 'timestamp')
admin.site.register(UserActivityLog, ShowUserActivityLog)


class ShowNotification(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'content', 'is_read', 'timestamp')
admin.site.register(Notification, ShowNotification)