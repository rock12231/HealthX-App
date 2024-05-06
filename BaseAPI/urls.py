from django.urls import path
from BaseAPI.views import DataDetail, DataList
from django.urls import path

urlpatterns = [
    path('data/', DataList.as_view()),
    path('data/<int:id>', DataDetail.as_view()),
]
