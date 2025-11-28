"""Forms for Tuina module."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import TuinaSession, TuinaSessionTechnique


class TuinaSessionForm(forms.ModelForm):
    """Form for creating/editing tuina sessions."""

    class Meta:
        model = TuinaSession
        fields = [
            'patient', 'session_date', 'chief_complaint', 'tcm_diagnosis',
            'treatment_principle', 'duration_minutes', 'primary_focus',
            'pain_level_before', 'pain_level_after',
            'mobility_before', 'mobility_after', 'patient_sensation',
            'immediate_effect', 'home_exercises', 'lifestyle_advice',
            'next_session_date', 'notes'
        ]
        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'next_session_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '120'}),
            'pain_level_before': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'pain_level_after': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tcm_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'treatment_principle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'primary_focus': forms.TextInput(attrs={'class': 'form-control'}),
            'mobility_before': forms.TextInput(attrs={'class': 'form-control'}),
            'mobility_after': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_sensation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'immediate_effect': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'home_exercises': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'lifestyle_advice': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
