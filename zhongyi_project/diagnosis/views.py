"""Views for Diagnosis System."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse

from patients.models import Patient
from .models import DiagnosisSession, Symptom, Syndrome
from .forms import (
    DiagnosisStep1Form, DiagnosisStep2Form, DiagnosisStep3Form,
    DiagnosisStep4Form, DiagnosisStep5Form, DiagnosisFinalForm
)
from .analysis import analyze_symptoms


class PractitionerRequiredMixin(UserPassesTestMixin):
    """Mixin to require practitioner or admin role."""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.role in ['practitioner', 'admin'] or
            self.request.user.is_staff
        )


class DiagnosisListView(LoginRequiredMixin, PractitionerRequiredMixin, ListView):
    """List all diagnosis sessions."""
    model = DiagnosisSession
    template_name = 'diagnosis/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        queryset = DiagnosisSession.objects.select_related('patient', 'practitioner')

        # Filter by practitioner for non-admin users
        if self.request.user.role == 'practitioner' and not self.request.user.is_staff:
            queryset = queryset.filter(practitioner=self.request.user)

        return queryset.order_by('-session_date')


class DiagnosisDetailView(LoginRequiredMixin, PractitionerRequiredMixin, DetailView):
    """View diagnosis session details."""
    model = DiagnosisSession
    template_name = 'diagnosis/session_detail.html'
    context_object_name = 'session'


@login_required
def select_patient(request):
    """Select a patient to start a new diagnosis."""
    patients = Patient.objects.filter(is_active=True).order_by('last_name', 'first_name')

    return render(request, 'diagnosis/select_patient.html', {
        'patients': patients,
    })


@login_required
def start_diagnosis(request, patient_pk):
    """Start a new diagnosis session for a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)

    if request.method == 'POST':
        form = DiagnosisStep1Form(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.patient = patient
            session.practitioner = request.user
            session.save()
            return redirect('diagnosis:step2', pk=session.pk)
    else:
        form = DiagnosisStep1Form()

    return render(request, 'diagnosis/step1_complaint.html', {
        'form': form,
        'patient': patient,
        'step': 1,
        'total_steps': 6,
    })


@login_required
def diagnosis_step2(request, pk):
    """Step 2: Inspection (望诊)."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    if request.method == 'POST':
        form = DiagnosisStep2Form(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('diagnosis:step3', pk=session.pk)
    else:
        form = DiagnosisStep2Form(instance=session)

    return render(request, 'diagnosis/step2_inspection.html', {
        'form': form,
        'session': session,
        'patient': session.patient,
        'step': 2,
        'total_steps': 6,
    })


@login_required
def diagnosis_step3(request, pk):
    """Step 3: Auscultation & Olfaction (闻诊)."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    if request.method == 'POST':
        form = DiagnosisStep3Form(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('diagnosis:step4', pk=session.pk)
    else:
        form = DiagnosisStep3Form(instance=session)

    return render(request, 'diagnosis/step3_auscultation.html', {
        'form': form,
        'session': session,
        'patient': session.patient,
        'step': 3,
        'total_steps': 6,
    })


@login_required
def diagnosis_step4(request, pk):
    """Step 4: Inquiry (问诊)."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    if request.method == 'POST':
        form = DiagnosisStep4Form(request.POST, instance=session)
        if form.is_valid():
            # Save selected symptoms
            symptoms = request.POST.getlist('symptoms')
            session.selected_symptoms = symptoms
            form.save()
            return redirect('diagnosis:step5', pk=session.pk)
    else:
        form = DiagnosisStep4Form(instance=session)
        # Pre-select previously selected symptoms
        if session.selected_symptoms:
            form.fields['symptoms'].initial = session.selected_symptoms

    # Group symptoms by category for display
    symptoms_by_category = {}
    for symptom in Symptom.objects.filter(is_active=True).order_by('category', 'name_en'):
        category = symptom.get_category_display()
        if category not in symptoms_by_category:
            symptoms_by_category[category] = []
        symptoms_by_category[category].append(symptom)

    return render(request, 'diagnosis/step4_inquiry.html', {
        'form': form,
        'session': session,
        'patient': session.patient,
        'symptoms_by_category': symptoms_by_category,
        'step': 4,
        'total_steps': 6,
    })


@login_required
def diagnosis_step5(request, pk):
    """Step 5: Palpation (切诊)."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    if request.method == 'POST':
        form = DiagnosisStep5Form(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('diagnosis:analyze', pk=session.pk)
    else:
        form = DiagnosisStep5Form(instance=session)

    return render(request, 'diagnosis/step5_palpation.html', {
        'form': form,
        'session': session,
        'patient': session.patient,
        'step': 5,
        'total_steps': 6,
    })


@login_required
def diagnosis_analyze(request, pk):
    """Step 6: AI Analysis and Final Diagnosis."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    # Run AI analysis
    tongue_data = {
        'body_color': session.tongue_body_color,
        'body_shape': session.tongue_body_shape,
        'coating_color': session.tongue_coating_color,
        'coating_texture': session.tongue_coating_texture,
    }

    pulse_data = {
        'overall': session.pulse_overall,
    }

    ai_results = analyze_symptoms(
        session.selected_symptoms,
        tongue_data=tongue_data,
        pulse_data=pulse_data
    )

    # Save AI results
    session.ai_suggested_syndromes = ai_results
    session.save()

    if request.method == 'POST':
        form = DiagnosisFinalForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.is_complete = True
            session.save()
            messages.success(
                request,
                _('Diagnosis session completed successfully! (诊断完成！)')
            )
            return redirect('diagnosis:detail', pk=session.pk)
    else:
        form = DiagnosisFinalForm(instance=session)
        # Pre-fill with AI suggestions if empty
        if not session.final_diagnosis and ai_results:
            suggested = ai_results[0]
            form.initial['final_diagnosis'] = f"{suggested['name_en']} ({suggested['name_cn']})"
            if suggested.get('treatment_principle'):
                form.initial['treatment_principle'] = suggested['treatment_principle']

    return render(request, 'diagnosis/step6_analyze.html', {
        'form': form,
        'session': session,
        'patient': session.patient,
        'ai_results': ai_results,
        'step': 6,
        'total_steps': 6,
    })


@login_required
def edit_diagnosis(request, pk):
    """Edit an existing diagnosis session."""
    session = get_object_or_404(DiagnosisSession, pk=pk)

    # Check permission - only admin, staff, or the original practitioner can edit
    if not (request.user.is_staff or request.user.role == 'admin' or session.practitioner == request.user):
        messages.error(request, _('您没有权限编辑此诊断记录。| You do not have permission to edit this diagnosis.'))
        return redirect('diagnosis:detail', pk=pk)

    # Group symptoms by category for display
    symptoms_by_category = {}
    for symptom in Symptom.objects.filter(is_active=True).order_by('category', 'name_en'):
        category = symptom.get_category_display()
        if category not in symptoms_by_category:
            symptoms_by_category[category] = []
        symptoms_by_category[category].append(symptom)

    if request.method == 'POST':
        # Update basic info
        session.chief_complaint = request.POST.get('chief_complaint', session.chief_complaint)
        session.final_diagnosis = request.POST.get('final_diagnosis', session.final_diagnosis)
        session.treatment_principle = request.POST.get('treatment_principle', session.treatment_principle)
        session.notes = request.POST.get('notes', session.notes)

        # Update tongue diagnosis
        session.tongue_body_color = request.POST.get('tongue_body_color', session.tongue_body_color)
        session.tongue_body_shape = request.POST.get('tongue_body_shape', session.tongue_body_shape)
        session.tongue_coating_color = request.POST.get('tongue_coating_color', session.tongue_coating_color)
        session.tongue_coating_texture = request.POST.get('tongue_coating_texture', session.tongue_coating_texture)

        # Update pulse
        session.pulse_overall = request.POST.get('pulse_overall', session.pulse_overall)

        # Update symptoms
        symptoms = request.POST.getlist('symptoms')
        session.selected_symptoms = symptoms

        session.save()

        messages.success(request, _('诊断记录已更新！| Diagnosis updated successfully!'))
        return redirect('diagnosis:detail', pk=pk)

    return render(request, 'diagnosis/edit_diagnosis.html', {
        'session': session,
        'patient': session.patient,
        'symptoms_by_category': symptoms_by_category,
    })


@login_required
def delete_diagnosis(request, pk):
    """Delete a diagnosis session (admin/staff only)."""
    session = get_object_or_404(DiagnosisSession, pk=pk)
    patient_pk = session.patient.pk

    # Check permission - only admin or staff can delete
    if not (request.user.is_staff or request.user.role == 'admin'):
        messages.error(request, _('您没有权限删除此诊断记录。| You do not have permission to delete this diagnosis.'))
        return redirect('diagnosis:detail', pk=pk)

    if request.method == 'POST':
        session.delete()
        messages.success(request, _('诊断记录已删除！| Diagnosis session deleted successfully!'))
        return redirect('patients:detail', pk=patient_pk)

    return render(request, 'diagnosis/confirm_delete.html', {
        'session': session,
    })


@login_required
def api_analyze_symptoms(request):
    """API endpoint for symptom analysis."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    symptoms = data.get('symptoms', [])
    tongue_data = data.get('tongue', {})
    pulse_data = data.get('pulse', {})

    results = analyze_symptoms(symptoms, tongue_data, pulse_data)

    return JsonResponse({
        'success': True,
        'results': results,
    })
