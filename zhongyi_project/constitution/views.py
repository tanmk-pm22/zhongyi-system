"""Views for Constitution module."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def constitution_list(request):
    """List all constitution types."""
    from .models import ConstitutionType

    constitutions = ConstitutionType.objects.filter(is_active=True).order_by('display_order')

    context = {
        'constitutions': constitutions,
        'title': _('体质类型 | Constitution Types'),
    }
    return render(request, 'constitution/constitution_list.html', context)


@login_required
def assessment_create(request, patient_id=None):
    """Create a new constitution assessment."""
    context = {
        'title': _('体质评估 | Constitution Assessment'),
    }
    return render(request, 'constitution/assessment_create.html', context)
