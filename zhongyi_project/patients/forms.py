"""Forms for Patient management."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Patient, MedicalRecord


class PatientForm(forms.ModelForm):
    """Form for creating/updating patients."""

    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name', 'chinese_name', 'ic_number',
            'date_of_birth', 'gender', 'blood_type', 'phone', 'email',
            'address', 'emergency_contact_name', 'emergency_contact_phone',
            'allergies', 'chronic_conditions', 'current_medications',
            'medical_history', 'family_history', 'tcm_constitution',
            'photo', 'notes', 'assigned_practitioner',
            'consent_data_sharing', 'consent_date'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'chinese_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ic_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tcm_constitution': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_practitioner': forms.Select(attrs={'class': 'form-select'}),
            'consent_data_sharing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consent_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PatientSearchForm(forms.Form):
    """Form for searching patients."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search by name, IC, phone... (搜索姓名、身份证、电话...)'),
        }),
    )


class MedicalRecordForm(forms.ModelForm):
    """Form for creating/updating medical records."""

    class Meta:
        model = MedicalRecord
        fields = (
            'record_type', 'visit_date', 'chief_complaint',
            'inspection_notes', 'tongue_diagnosis',
            'auscultation_notes', 'inquiry_notes',
            'pulse_diagnosis', 'palpation_notes',
            'tcm_diagnosis', 'western_diagnosis',
            'treatment_principle', 'prescription',
            'acupuncture_points', 'other_treatments',
            'lifestyle_advice', 'dietary_advice',
            'follow_up_notes', 'next_appointment'
        )
        widgets = {
            'record_type': forms.Select(attrs={'class': 'form-select'}),
            'visit_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inspection_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tongue_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'auscultation_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'inquiry_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pulse_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'palpation_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tcm_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'western_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_principle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'acupuncture_points': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'other_treatments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lifestyle_advice': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dietary_advice': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'next_appointment': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
