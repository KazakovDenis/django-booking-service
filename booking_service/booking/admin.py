from django.contrib import admin

from .models import Appointment, Doctor


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty')
    list_filter = ('specialty', 'user')
    search_fields = ('specialty', 'user')
    fields = ('user', 'specialty')

    inlines = [
        AppointmentInline,
    ]
