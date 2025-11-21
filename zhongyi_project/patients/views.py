"""Views for Patient management."""
import io
import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.db.models import Q

from .models import Patient, MedicalRecord
from .forms import PatientForm, PatientSearchForm, MedicalRecordForm


class PractitionerRequiredMixin(UserPassesTestMixin):
    """Mixin to require practitioner or admin role."""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_practitioner or
            self.request.user.is_admin or
            self.request.user.is_staff
        )


class PatientListView(LoginRequiredMixin, PractitionerRequiredMixin, ListView):
    """List all patients with search functionality."""
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        queryset = Patient.objects.filter(is_active=True)

        # Filter by assigned practitioner for non-admin users
        if self.request.user.is_practitioner and not self.request.user.is_staff:
            queryset = queryset.filter(assigned_practitioner=self.request.user)

        # Search functionality
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(chinese_name__icontains=search_query) |
                Q(ic_number__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        return queryset.select_related('assigned_practitioner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PatientSearchForm(self.request.GET)
        return context


class PatientDetailView(LoginRequiredMixin, PractitionerRequiredMixin, DetailView):
    """View patient details and medical records."""
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show latest medical records first
        context['medical_records'] = self.object.medical_records.select_related('practitioner').order_by('-visit_date')[:10]
        return context


class PatientCreateView(LoginRequiredMixin, PractitionerRequiredMixin, CreateView):
    """Create a new patient."""
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def form_valid(self, form):
        # Auto-assign current practitioner if not specified
        if not form.cleaned_data.get('assigned_practitioner') and self.request.user.is_practitioner:
            form.instance.assigned_practitioner = self.request.user

        messages.success(
            self.request,
            _('Patient created successfully! (患者创建成功！)')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:detail', kwargs={'pk': self.object.pk})


class PatientUpdateView(LoginRequiredMixin, PractitionerRequiredMixin, UpdateView):
    """Update patient information."""
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Patient updated successfully! (患者信息更新成功！)')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:detail', kwargs={'pk': self.object.pk})


class PatientDeleteView(LoginRequiredMixin, PractitionerRequiredMixin, DeleteView):
    """Soft delete a patient (set is_active=False)."""
    model = Patient
    template_name = 'patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patients:list')

    def form_valid(self, form):
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(
            self.request,
            _('Patient archived successfully. (患者已归档。)')
        )
        return redirect(self.success_url)


@login_required
def patient_qrcode(request, pk):
    """Generate QR code for patient identification."""
    patient = get_object_or_404(Patient, pk=pk)

    # Generate QR code with patient ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(patient.patient_id))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Return as PNG image
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


# Medical Record Views

class MedicalRecordCreateView(LoginRequiredMixin, PractitionerRequiredMixin, CreateView):
    """Create a new medical record for a patient."""
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'patients/medicalrecord_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context

    def form_valid(self, form):
        form.instance.patient = self.patient
        form.instance.practitioner = self.request.user
        messages.success(
            self.request,
            _('Medical record created successfully! (病历创建成功！)')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:detail', kwargs={'pk': self.patient.pk})


class MedicalRecordUpdateView(LoginRequiredMixin, PractitionerRequiredMixin, UpdateView):
    """Update a medical record."""
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'patients/medicalrecord_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Medical record updated successfully! (病历更新成功！)')
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:detail', kwargs={'pk': self.object.patient.pk})


class MedicalRecordDetailView(LoginRequiredMixin, PractitionerRequiredMixin, DetailView):
    """View medical record details."""
    model = MedicalRecord
    template_name = 'patients/medicalrecord_detail.html'
    context_object_name = 'record'
