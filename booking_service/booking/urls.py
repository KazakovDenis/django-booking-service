from django.urls import path

from .views import AppointmentView

urlpatterns = [
    path('', AppointmentView.as_view(), name='appointment'),
]
