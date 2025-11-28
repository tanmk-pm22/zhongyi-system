"""Views for Cupping module."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def cupping_session_list(request):
    """List all cupping sessions."""
    context = {
        'title': _('拔罐记录 | Cupping Sessions'),
    }
    return render(request, 'cupping/session_list.html', context)
