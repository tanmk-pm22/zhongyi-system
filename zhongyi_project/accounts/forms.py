"""Forms for user authentication and registration."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    role = forms.ChoiceField(
        choices=[
            (User.Role.PATIENT, _('Patient (患者)')),
            (User.Role.PRACTITIONER, _('TCM Practitioner (中医师)')),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Register as'),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username'),
        }),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        }),
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone',
            'ic_number', 'date_of_birth', 'address', 'profile_photo',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'ic_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PractitionerProfileForm(UserProfileForm):
    """Extended profile form for practitioners."""

    class Meta(UserProfileForm.Meta):
        fields = UserProfileForm.Meta.fields + (
            'license_number', 'specialization', 'clinic_name',
        )
        widgets = {
            **UserProfileForm.Meta.widgets,
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
