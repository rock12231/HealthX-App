from django.urls import path
from Profile.views import Login, Register, Logout ,Patient , Doctor , UpdateNotification 

urlpatterns = [
    path('login/',Login.as_view(), name='login'),
    path('logout/',Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('patient/', Patient.as_view(), name='patient'),
    path('patient/<int:pk>/', UpdateNotification, name='notiupdate'),
    path('doctor/', Doctor.as_view(), name='doctor'),
    
]

