from django.views.generic.edit import FormView

from .forms import AppointmentForm


class AppointmentView(FormView):
    template_name = 'booking.html'
    form_class = AppointmentForm
    success_url = ''
