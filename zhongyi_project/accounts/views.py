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


@login_required
def patient_portal_dashboard(request):
    """
    Patient portal dashboard view.
    患者门户仪表板视图
    """
    # Check if user has a patient profile
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, _('您没有患者档案。请联系诊所管理员。| You do not have a patient profile. Please contact the clinic administrator.'))
        return redirect('accounts:dashboard')

    patient = request.user.patient_profile

    from prescriptions.models import Prescription
    from diagnosis.models import DiagnosisSession
    from patients.models import MedicalRecord
    from django.utils import timezone
    from datetime import timedelta

    # Get recent prescriptions
    recent_prescriptions = Prescription.objects.filter(
        patient=patient
    ).select_related('practitioner').order_by('-prescription_date')[:5]

    # Get recent diagnoses
    recent_diagnoses = DiagnosisSession.objects.filter(
        patient=patient
    ).select_related('practitioner').order_by('-session_date')[:5]

    # Get recent medical records
    recent_records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related('practitioner').order_by('-visit_date')[:5]

    # Get statistics
    total_prescriptions = Prescription.objects.filter(patient=patient).count()
    total_diagnoses = DiagnosisSession.objects.filter(patient=patient).count()
    total_visits = MedicalRecord.objects.filter(patient=patient).count()

    # Get recent activity (last 30 days)
    month_ago = timezone.now() - timedelta(days=30)
    recent_activity_count = (
        Prescription.objects.filter(patient=patient, prescription_date__gte=month_ago).count() +
        DiagnosisSession.objects.filter(patient=patient, session_date__gte=month_ago).count()
    )

    # Health tips based on constitution
    health_tips = _get_health_tips_for_constitution(patient.tcm_constitution)

    context = {
        'patient': patient,
        'recent_prescriptions': recent_prescriptions,
        'recent_diagnoses': recent_diagnoses,
        'recent_records': recent_records,
        'total_prescriptions': total_prescriptions,
        'total_diagnoses': total_diagnoses,
        'total_visits': total_visits,
        'recent_activity_count': recent_activity_count,
        'health_tips': health_tips,
    }

    return render(request, 'accounts/patient_portal_dashboard.html', context)


@login_required
def patient_prescription_history(request):
    """
    View patient's prescription history.
    查看患者处方历史
    """
    # Check if user has a patient profile
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, _('您没有患者档案。| You do not have a patient profile.'))
        return redirect('accounts:dashboard')

    patient = request.user.patient_profile

    from prescriptions.models import Prescription

    prescriptions = Prescription.objects.filter(
        patient=patient
    ).select_related('practitioner').prefetch_related('items__herb', 'patent_medicine_items__medicine').order_by('-prescription_date')

    context = {
        'patient': patient,
        'prescriptions': prescriptions,
    }

    return render(request, 'accounts/patient_prescription_history.html', context)


@login_required
def patient_appointment_history(request):
    """
    View patient's appointment and visit history.
    查看患者预约和就诊历史
    """
    # Check if user has a patient profile
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, _('您没有患者档案。| You do not have a patient profile.'))
        return redirect('accounts:dashboard')

    patient = request.user.patient_profile

    from patients.models import MedicalRecord
    from diagnosis.models import DiagnosisSession

    medical_records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related('practitioner').order_by('-visit_date')

    diagnosis_sessions = DiagnosisSession.objects.filter(
        patient=patient
    ).select_related('practitioner').order_by('-session_date')

    context = {
        'patient': patient,
        'medical_records': medical_records,
        'diagnosis_sessions': diagnosis_sessions,
    }

    return render(request, 'accounts/patient_appointment_history.html', context)


def _get_health_tips_for_constitution(constitution):
    """
    Get health tips based on TCM constitution.
    根据中医体质获取健康建议
    """
    tips_dict = {
        '气虚质': [
            '饮食宜清淡，多食用健脾益气的食物，如山药、大枣、扁豆等。| Diet should be light, eat more foods that strengthen spleen and tonify qi, such as yam, jujube, lentils.',
            '适当运动，避免剧烈运动，推荐太极拳、八段锦等温和运动。| Moderate exercise, avoid vigorous exercise, recommend Tai Chi, Ba Duan Jin and other gentle exercises.',
            '保证充足睡眠，避免过度劳累。| Ensure adequate sleep and avoid overwork.',
            '保持心情愉悦，避免过度思虑。| Maintain a happy mood and avoid overthinking.'
        ],
        '阳虚质': [
            '饮食宜温热，多食用温阳补肾的食物，如羊肉、韭菜、核桃等。| Diet should be warm, eat more yang-tonifying foods such as mutton, leeks, walnuts.',
            '注意保暖，避免受寒。| Keep warm and avoid cold.',
            '可常晒太阳，促进阳气生发。| Regular sun exposure helps generate yang qi.',
            '适当运动，增强体质。| Moderate exercise to strengthen constitution.'
        ],
        '阴虚质': [
            '饮食宜清润，多食用滋阴润燥的食物，如百合、银耳、梨等。| Diet should be nourishing, eat more yin-nourishing foods such as lily, white fungus, pear.',
            '避免熬夜，保证充足睡眠。| Avoid staying up late, ensure adequate sleep.',
            '少食辛辣燥热食物。| Reduce spicy and heat-producing foods.',
            '保持环境湿润，避免干燥。| Keep environment moist, avoid dryness.'
        ],
        '痰湿质': [
            '饮食宜清淡，少食甜腻、油炸食物。| Diet should be light, reduce sweet, greasy, fried foods.',
            '多食用健脾化湿的食物，如薏米、冬瓜、海带等。| Eat more spleen-strengthening and dampness-resolving foods like Job\'s tears, winter melon, kelp.',
            '适当运动，促进代谢。| Regular exercise to promote metabolism.',
            '避免潮湿环境。| Avoid damp environments.'
        ],
        '湿热质': [
            '饮食宜清淡，多食用清热利湿的食物，如绿豆、苦瓜、莲藕等。| Diet should be light, eat heat-clearing and dampness-draining foods like mung beans, bitter gourd, lotus root.',
            '避免辛辣、油腻、甜食。| Avoid spicy, greasy, and sweet foods.',
            '保持环境通风干燥。| Keep environment ventilated and dry.',
            '适当运动，促进排汗。| Regular exercise to promote sweating.'
        ],
        '血瘀质': [
            '饮食宜活血化瘀，多食用山楂、黑木耳、洋葱等。| Diet should promote blood circulation, eat more hawthorn, black fungus, onion.',
            '适当运动，促进血液循环。| Regular exercise to promote blood circulation.',
            '保持心情舒畅，避免情绪郁结。| Maintain good mood, avoid emotional stagnation.',
            '注意保暖，避免受寒。| Keep warm and avoid cold.'
        ],
        '气郁质': [
            '饮食宜疏肝理气，多食用佛手、玫瑰花、柑橘等。| Diet should soothe liver and regulate qi, eat more bergamot, rose, citrus.',
            '保持心情愉悦，多参加社交活动。| Maintain happy mood, participate in social activities.',
            '适当运动，如散步、瑜伽等。| Moderate exercise like walking, yoga.',
            '培养兴趣爱好，释放压力。| Cultivate hobbies to release stress.'
        ],
        '特禀质': [
            '饮食要注意避免过敏源。| Pay attention to avoid allergens in diet.',
            '增强体质，适当运动。| Strengthen constitution with moderate exercise.',
            '避免接触过敏物质。| Avoid contact with allergic substances.',
            '保持环境清洁，减少过敏原。| Keep environment clean to reduce allergens.'
        ],
        '平和质': [
            '保持均衡饮食，营养丰富。| Maintain balanced diet with rich nutrition.',
            '规律作息，适量运动。| Regular routine and moderate exercise.',
            '保持良好心态，情绪稳定。| Maintain good mindset and emotional stability.',
            '预防为主，定期体检。| Focus on prevention, regular health checkups.'
        ]
    }

    # Return tips for the constitution, or general tips if not found
    return tips_dict.get(constitution, tips_dict['平和质'])
