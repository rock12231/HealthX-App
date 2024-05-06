from django.contrib import admin
from Predict.models import ChatModel
# Register your models here.


class ShowChatModel(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'timestamp')

admin.site.register(ChatModel, ShowChatModel)
