from django.contrib import admin
from BaseAPI.models import DataModel
# Register your models here.

class ShowDataModel(admin.ModelAdmin):
    list_display = ('id','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slop','ca','thal','created_at')

admin.site.register(DataModel, ShowDataModel)