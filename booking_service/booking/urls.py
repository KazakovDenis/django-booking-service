from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookingView.as_view(), name='booking'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('schedule/<int:id>', views.get_doctor_appointments, name='schedule'),
]
