"""Views for Treatment Course module."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

@login_required
def course_list(request):
    """List all treatment courses."""
    context = {
        'title': _('治疗疗程 | Treatment Courses'),
    }
    return render(request, 'treatment_course/course_list.html', context)
