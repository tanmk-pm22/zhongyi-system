from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import AcupunctureSession, AcupointReference
from .forms import AcupunctureSessionForm


class PractitionerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Require user to be practitioner or admin."""
    def test_func(self):
        return self.request.user.is_practitioner or self.request.user.is_admin


class AcupunctureSessionListView(PractitionerRequiredMixin, ListView):
    model = AcupunctureSession
    template_name = 'acupuncture/acupuncturesession_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        queryset = AcupunctureSession.objects.filter(is_active=True).select_related('patient', 'assigned_practitioner')

        # Filter by practitioner for non-admin users
        if self.request.user.is_practitioner and not self.request.user.is_admin:
            queryset = queryset.filter(assigned_practitioner=self.request.user)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__chinese_name__icontains=search) |
                Q(chief_complaint__icontains=search) |
                Q(tcm_diagnosis__icontains=search) |
                Q(acupoints_used__icontains=search)
            )

        return queryset.order_by('-session_date', '-created_at')


class AcupunctureSessionDetailView(PractitionerRequiredMixin, DetailView):
    model = AcupunctureSession
    template_name = 'acupuncture/acupuncturesession_detail.html'
    context_object_name = 'session'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('patient', 'assigned_practitioner')


class AcupunctureSessionCreateView(PractitionerRequiredMixin, CreateView):
    model = AcupunctureSession
    form_class = AcupunctureSessionForm
    template_name = 'acupuncture/acupuncturesession_form.html'
    success_url = reverse_lazy('acupuncture:list')

    def form_valid(self, form):
        form.instance.assigned_practitioner = self.request.user
        messages.success(self.request, _('针灸治疗记录已创建 | Acupuncture session created successfully'))
        return super().form_valid(form)


class AcupunctureSessionUpdateView(PractitionerRequiredMixin, UpdateView):
    model = AcupunctureSession
    form_class = AcupunctureSessionForm
    template_name = 'acupuncture/acupuncturesession_form.html'
    success_url = reverse_lazy('acupuncture:list')

    def form_valid(self, form):
        messages.success(self.request, _('针灸治疗记录已更新 | Acupuncture session updated successfully'))
        return super().form_valid(form)


class AcupunctureSessionDeleteView(PractitionerRequiredMixin, DeleteView):
    model = AcupunctureSession
    template_name = 'acupuncture/acupuncturesession_confirm_delete.html'
    success_url = reverse_lazy('acupuncture:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, _('针灸治疗记录已删除 | Acupuncture session deleted successfully'))
        return redirect(self.success_url)


class AcupointLibraryView(PractitionerRequiredMixin, ListView):
    """穴位图库 | Acupoint Library"""
    model = AcupointReference
    template_name = 'acupuncture/acupoint_library.html'
    context_object_name = 'acupoints'
    paginate_by = 20

    def get_queryset(self):
        queryset = AcupointReference.objects.filter(is_active=True)

        # Filter by meridian
        meridian = self.request.GET.get('meridian')
        if meridian:
            queryset = queryset.filter(meridian=meridian)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(chinese_name__icontains=search) |
                Q(pinyin_name__icontains=search) |
                Q(english_name__icontains=search) |
                Q(indications__icontains=search)
            )

        return queryset.order_by('meridian', 'code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meridian_choices'] = AcupointReference.MeridianType.choices
        context['selected_meridian'] = self.request.GET.get('meridian', '')
        return context


class AcupointDetailView(PractitionerRequiredMixin, DetailView):
    """穴位详情 | Acupoint Detail"""
    model = AcupointReference
    template_name = 'acupuncture/acupoint_detail.html'
    context_object_name = 'acupoint'
    slug_field = 'code'
    slug_url_kwarg = 'code'
