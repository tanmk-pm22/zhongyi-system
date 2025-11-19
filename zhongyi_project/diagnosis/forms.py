"""Forms for Diagnosis System."""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import DiagnosisSession, Symptom, TongueAppearance, PulseQuality


class DiagnosisStep1Form(forms.ModelForm):
    """Step 1: Chief Complaint and Basic Info."""

    class Meta:
        model = DiagnosisSession
        fields = ['chief_complaint']
        widgets = {
            'chief_complaint': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Describe the main complaint and symptoms...'),
            }),
        }


class DiagnosisStep2Form(forms.ModelForm):
    """Step 2: Inspection (望诊)."""

    class Meta:
        model = DiagnosisSession
        fields = [
            'spirit_status', 'complexion',
            'tongue_body_color', 'tongue_body_shape',
            'tongue_coating_color', 'tongue_coating_texture', 'tongue_notes'
        ]
        widgets = {
            'spirit_status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('alert', _('Alert and Bright (神清气爽)')),
                ('normal', _('Normal (正常)')),
                ('listless', _('Listless (萎靡)')),
                ('agitated', _('Agitated (烦躁)')),
                ('confused', _('Confused (神昏)')),
            ]),
            'complexion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal/Rosy (正常)')),
                ('pale', _('Pale (苍白)')),
                ('sallow', _('Sallow/Yellow (萎黄)')),
                ('red', _('Red (红赤)')),
                ('dark', _('Dark/Dull (晦暗)')),
                ('blue', _('Bluish (青紫)')),
            ]),
            'tongue_body_color': forms.Select(attrs={'class': 'form-select'}),
            'tongue_body_shape': forms.Select(attrs={'class': 'form-select'}),
            'tongue_coating_color': forms.Select(attrs={'class': 'form-select'}),
            'tongue_coating_texture': forms.Select(attrs={'class': 'form-select'}),
            'tongue_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DiagnosisStep3Form(forms.ModelForm):
    """Step 3: Auscultation & Olfaction (闻诊)."""

    class Meta:
        model = DiagnosisSession
        fields = ['voice_quality', 'breath_odor', 'auscultation_notes']
        widgets = {
            'voice_quality': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('loud', _('Loud/Coarse (声高)')),
                ('weak', _('Weak/Low (声低)')),
                ('hoarse', _('Hoarse (嘶哑)')),
            ]),
            'breath_odor': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('foul', _('Foul/Bad (臭秽)')),
                ('sour', _('Sour (酸腐)')),
                ('none', _('None/Absent (无味)')),
            ]),
            'auscultation_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DiagnosisStep4Form(forms.ModelForm):
    """Step 4: Inquiry (问诊)."""

    symptoms = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label=_('Select Symptoms'),
    )

    class Meta:
        model = DiagnosisSession
        fields = [
            'symptom_details', 'sleep_quality', 'appetite', 'thirst',
            'defecation', 'urination', 'perspiration', 'inquiry_notes'
        ]
        widgets = {
            'symptom_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sleep_quality': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('good', _('Good (好)')),
                ('difficulty_falling', _('Difficulty falling asleep (难以入睡)')),
                ('light', _('Light/Easily woken (易醒)')),
                ('dream_disturbed', _('Dream-disturbed (多梦)')),
                ('insomnia', _('Insomnia (失眠)')),
                ('excessive', _('Excessive (嗜睡)')),
            ]),
            'appetite': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('poor', _('Poor (食欲不振)')),
                ('excessive', _('Excessive (食欲亢进)')),
                ('preference_cold', _('Prefers cold food (喜冷食)')),
                ('preference_hot', _('Prefers hot food (喜热食)')),
            ]),
            'thirst': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('no_thirst', _('No thirst (口不渴)')),
                ('preference_cold', _('Prefers cold drinks (喜冷饮)')),
                ('preference_hot', _('Prefers hot drinks (喜热饮)')),
                ('dry_mouth', _('Dry mouth (口干)')),
            ]),
            'defecation': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('constipation', _('Constipation (便秘)')),
                ('loose', _('Loose stools (便溏)')),
                ('diarrhea', _('Diarrhea (腹泻)')),
                ('dry', _('Dry stools (大便干)')),
            ]),
            'urination': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('frequent', _('Frequent (尿频)')),
                ('scanty', _('Scanty (尿少)')),
                ('dark', _('Dark yellow (尿黄)')),
                ('clear', _('Clear and profuse (清长)')),
                ('nocturia', _('Nocturia (夜尿)')),
            ]),
            'perspiration': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', _('Select...')),
                ('normal', _('Normal (正常)')),
                ('spontaneous', _('Spontaneous (自汗)')),
                ('night', _('Night sweating (盗汗)')),
                ('profuse', _('Profuse (大汗)')),
                ('none', _('No sweating (无汗)')),
            ]),
            'inquiry_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load symptoms grouped by category
        symptoms = Symptom.objects.filter(is_active=True).order_by('category', 'name_en')
        choices = [(s.code, f"{s.name_en} ({s.name_cn})") for s in symptoms]
        self.fields['symptoms'].choices = choices


class DiagnosisStep5Form(forms.ModelForm):
    """Step 5: Palpation (切诊)."""

    PULSE_CHOICES = [('', _('Select...'))] + list(PulseQuality.PulseType.choices)

    class Meta:
        model = DiagnosisSession
        fields = [
            'pulse_left_cun', 'pulse_left_guan', 'pulse_left_chi',
            'pulse_right_cun', 'pulse_right_guan', 'pulse_right_chi',
            'pulse_overall', 'palpation_notes'
        ]
        widgets = {
            'pulse_left_cun': forms.Select(attrs={'class': 'form-select'}),
            'pulse_left_guan': forms.Select(attrs={'class': 'form-select'}),
            'pulse_left_chi': forms.Select(attrs={'class': 'form-select'}),
            'pulse_right_cun': forms.Select(attrs={'class': 'form-select'}),
            'pulse_right_guan': forms.Select(attrs={'class': 'form-select'}),
            'pulse_right_chi': forms.Select(attrs={'class': 'form-select'}),
            'pulse_overall': forms.TextInput(attrs={'class': 'form-control'}),
            'palpation_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['pulse_left_cun', 'pulse_left_guan', 'pulse_left_chi',
                      'pulse_right_cun', 'pulse_right_guan', 'pulse_right_chi']:
            self.fields[field].widget.choices = self.PULSE_CHOICES


class DiagnosisFinalForm(forms.ModelForm):
    """Final step: Review AI suggestions and confirm diagnosis."""

    class Meta:
        model = DiagnosisSession
        fields = ['final_diagnosis', 'treatment_principle', 'notes']
        widgets = {
            'final_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'treatment_principle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
