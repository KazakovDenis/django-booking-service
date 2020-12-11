from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView

from .forms import AppointmentForm
from .models import Appointment


class BookingView(FormView):
    """Endpoint для работы с формой записи на приём"""
    form_class = AppointmentForm
    template_name = 'booking.html'
    success_url = '/success/'

    def form_valid(self, form):
        """Сохранить Приём у врача и направить на страницу успешной записи"""
        instance = form.save()
        url = '%s?id=%s' % (self.get_success_url(), instance.id)
        return HttpResponseRedirect(url)


class SuccessView(TemplateView):
    """Endpoint для показа информации об успешной записи на приём"""
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_id = self.request.GET.get('id')
        if not app_id:
            raise Http404(_('Такой страницы не существует'))
        context['appointment'] = get_object_or_404(Appointment, pk=app_id)
        return context
