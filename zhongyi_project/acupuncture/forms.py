from django import forms
from django.utils.translation import gettext_lazy as _
from .models import AcupunctureSession


class AcupunctureSessionForm(forms.ModelForm):
    class Meta:
        model = AcupunctureSession
        fields = (
            'patient',
            'session_date',
            'treatment_type',
            'chief_complaint',
            'tcm_diagnosis',
            'acupoints_used',
            'needle_retention_time',
            'technique_notes',
            'used_moxibustion',
            'used_cupping',
            'used_tuina',
            'patient_response',
            'treatment_notes',
            'next_session_date',
            'treatment_plan',
            'session_fee',
        )
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-select',
            }),
            'session_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'treatment_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'chief_complaint': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('例如：颈肩疼痛、失眠、头痛等 | e.g., Neck and shoulder pain, insomnia, headaches, etc.')
            }),
            'tcm_diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('例如：气滞血瘀、肝阳上亢等 | e.g., Qi stagnation and blood stasis, Liver Yang rising, etc.')
            }),
            'acupoints_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('例如：合谷(LI4), 太冲(LR3), 足三里(ST36), 百会(GV20) | e.g., Hegu (LI4), Taichong (LR3), Zusanli (ST36), Baihui (GV20)')
            }),
            'needle_retention_time': forms.Select(attrs={
                'class': 'form-select',
            }),
            'technique_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('例如：提插捻转、平补平泻、留针得气等 | e.g., Lifting-thrusting, reinforcing-reducing, needle sensation achieved, etc.')
            }),
            'used_moxibustion': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'used_cupping': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'used_tuina': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'patient_response': forms.Select(attrs={
                'class': 'form-select',
            }),
            'treatment_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('患者反馈、注意事项、建议等 | Patient feedback, precautions, recommendations, etc.')
            }),
            'next_session_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'treatment_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('下次治疗计划和建议 | Next treatment plan and recommendations')
            }),
            'session_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': _('马币 | MYR')
            }),
        }
