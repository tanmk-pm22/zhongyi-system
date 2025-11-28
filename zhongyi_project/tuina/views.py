"""Views for Tuina module."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import TuinaSession, TuinaTechnique
from .forms import TuinaSessionForm


@login_required
def tuina_session_list(request):
    """List all tuina sessions."""
    sessions = TuinaSession.objects.filter(is_active=True).select_related('patient', 'practitioner').order_by('-session_date')

    # Filter by patient if specified
    patient_id = request.GET.get('patient')
    if patient_id:
        sessions = sessions.filter(patient_id=patient_id)

    context = {
        'title': _('推拿记录 | Tuina Sessions'),
        'sessions': sessions,
    }
    return render(request, 'tuina/session_list.html', context)


@login_required
def tuina_session_create(request, patient_id=None):
    """Create a new tuina session."""
    if request.method == 'POST':
        form = TuinaSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.practitioner = request.user
            session.save()
            messages.success(request, _('推拿记录创建成功！| Tuina session created successfully!'))
            return redirect('tuina:session_detail', pk=session.pk)
    else:
        initial = {}
        if patient_id:
            initial['patient'] = patient_id
        initial['session_date'] = timezone.now()
        form = TuinaSessionForm(initial=initial)

    context = {
        'title': _('新建推拿记录 | New Tuina Session'),
        'form': form,
    }
    return render(request, 'tuina/session_form.html', context)


@login_required
def tuina_session_detail(request, pk):
    """View tuina session details."""
    session = get_object_or_404(TuinaSession, pk=pk, is_active=True)

    context = {
        'title': _('推拿记录详情 | Tuina Session Details'),
        'session': session,
    }
    return render(request, 'tuina/session_detail.html', context)


@login_required
def tuina_session_edit(request, pk):
    """Edit a tuina session."""
    session = get_object_or_404(TuinaSession, pk=pk, is_active=True)

    if request.method == 'POST':
        form = TuinaSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, _('推拿记录更新成功！| Tuina session updated successfully!'))
            return redirect('tuina:session_detail', pk=session.pk)
    else:
        form = TuinaSessionForm(instance=session)

    context = {
        'title': _('编辑推拿记录 | Edit Tuina Session'),
        'form': form,
        'session': session,
    }
    return render(request, 'tuina/session_form.html', context)


@login_required
def tuina_session_delete(request, pk):
    """Delete (soft delete) a tuina session."""
    session = get_object_or_404(TuinaSession, pk=pk, is_active=True)

    if request.method == 'POST':
        session.is_active = False
        session.save()
        messages.success(request, _('推拿记录已删除 | Tuina session deleted'))
        return redirect('tuina:session_list')

    context = {
        'title': _('删除推拿记录 | Delete Tuina Session'),
        'session': session,
    }
    return render(request, 'tuina/session_confirm_delete.html', context)
