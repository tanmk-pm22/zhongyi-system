"""Views for Appointments module."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def appointment_list(request):
    """List all appointments."""
    context = {
        'title': _('预约管理 | Appointments'),
    }
    return render(request, 'appointments/appointment_list.html', context)


@login_required
def appointment_calendar(request):
    """Calendar view of appointments."""
    context = {
        'title': _('预约日历 | Appointment Calendar'),
    }
    return render(request, 'appointments/appointment_calendar.html', context)
