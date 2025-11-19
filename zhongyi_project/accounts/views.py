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
    context = {
        'user': request.user,
    }

    if request.user.is_practitioner:
        # Get practitioner's patients
        from patients.models import Patient
        context['patients'] = Patient.objects.filter(
            assigned_practitioner=request.user
        ).order_by('-updated_at')[:10]
        context['patient_count'] = Patient.objects.filter(
            assigned_practitioner=request.user
        ).count()

    return render(request, 'accounts/dashboard.html', context)
