from django.urls import path
from Predict.views import Prediction, Prescription

urlpatterns = [
    # path('resetpass/<str:url>', ResetPassView.as_view(), name='resetpass'),
    # path('predict/<str:link>',Prediction.as_view(), name="predict"),
    path('doctor/predict/<str:link>',Prediction.as_view(), name="predict"),
    path('doctor/prescription/<str:link>',Prescription.as_view(), name="prescription"),
    path('patient/prescription/<str:link>',Prescription.as_view(), name="pprescription"),
]