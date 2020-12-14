from django.contrib import admin

from .models import Appointment, Doctor


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialty')
    list_filter = ('specialty',)
    search_fields = ('specialty', 'user__first_name', 'user__last_name')
    ordering = ('specialty', 'user__last_name')

    fields = ('specialty', 'user', 'full_name')
    readonly_fields = ('full_name',)

    inlines = [
        AppointmentInline
    ]
