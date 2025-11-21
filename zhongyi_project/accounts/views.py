"""Views for user authentication."""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PractitionerProfileForm


class RegisterView(CreateView):
    """User registration view."""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            _('Account created successfully! Please login. (账户创建成功！请登录。)')
        )
        return response


class CustomLoginView(LoginView):
    """Custom login view with styled form."""
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Welcome back! (欢迎回来！)')
        )
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""

    def dispatch(self, request, *args, **kwargs):
        messages.info(
            request,
            _('You have been logged out. (您已退出登录。)')
        )
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """User profile view."""
    model = User
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def get_form_class(self):
        if self.request.user.is_practitioner:
            return PractitionerProfileForm
        return UserProfileForm

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Profile updated successfully! (个人资料更新成功！)')
        )
        return super().form_valid(form)


@login_required
def dashboard_view(request):
    """Dashboard view based on user role."""
    from patients.models import Patient, MedicalRecord
    from prescriptions.models import Prescription
    from diagnosis.models import DiagnosisSession
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count, Q

    context = {
        'user': request.user,
    }

    if request.user.is_practitioner or request.user.is_admin or request.user.is_staff:
        # Filter by practitioner for non-admin users
        if request.user.is_practitioner and not request.user.is_staff:
            patient_filter = Q(assigned_practitioner=request.user)
            prescription_filter = Q(practitioner=request.user)
            diagnosis_filter = Q(practitioner=request.user)
        else:
            patient_filter = Q()
            prescription_filter = Q()
            diagnosis_filter = Q()

        # Get patient statistics
        patients = Patient.objects.filter(patient_filter)
        context['patient_count'] = patients.count()
        context['active_patient_count'] = patients.filter(is_active=True).count()

        # Get recent patients (last 10)
        context['patients'] = patients.order_by('-updated_at')[:10]

        # Get diagnosis statistics
        diagnoses = DiagnosisSession.objects.filter(diagnosis_filter)
        context['diagnosis_count'] = diagnoses.count()

        # Get prescription statistics
        prescriptions = Prescription.objects.filter(prescription_filter)
        context['prescription_count'] = prescriptions.count()

        # Get time-based statistics (last 7 days, 30 days)
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        context['prescriptions_this_week'] = prescriptions.filter(
            prescription_date__gte=week_ago
        ).count()

        context['prescriptions_this_month'] = prescriptions.filter(
            prescription_date__gte=month_ago
        ).count()

        context['diagnoses_this_week'] = diagnoses.filter(
            session_date__gte=week_ago
        ).count()

        context['diagnoses_this_month'] = diagnoses.filter(
            session_date__gte=month_ago
        ).count()

        # Get recent prescriptions (last 5)
        context['recent_prescriptions'] = prescriptions.select_related(
            'patient', 'practitioner'
        ).order_by('-prescription_date')[:5]

        # Get recent diagnoses (last 5)
        context['recent_diagnoses'] = diagnoses.select_related(
            'patient', 'practitioner'
        ).order_by('-session_date')[:5]

    return render(request, 'accounts/dashboard.html', context)
