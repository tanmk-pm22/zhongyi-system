from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden
from django.utils import timezone

from patients.models import Patient, MedicalRecord
from prescriptions.models import Prescription
from booking.models import Appointment
from acupuncture.models import AcupunctureSession


def get_patient_or_403(request):
    """获取患者档案或返回403 | Get patient or return 403"""
    try:
        return Patient.objects.get(user_account=request.user)
    except Patient.DoesNotExist:
        return None


@login_required
def dashboard(request):
    """患者中心 | Patient Dashboard"""
    patient = get_patient_or_403(request)
    if not patient:
        messages.warning(request, _('您还没有患者档案。请联系诊所创建档案。| You don\'t have a patient profile yet. Please contact the clinic to create one.'))
        return redirect('website:home')

    # 获取概览数据
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=['pending', 'confirmed'],
        appointment_date__gte=timezone.now().date()
    ).order_by('appointment_date', 'appointment_time')[:3]

    recent_records = MedicalRecord.objects.filter(
        patient=patient,
        is_active=True
    ).order_by('-visit_date')[:5]

    recent_prescriptions = Prescription.objects.filter(
        patient=patient,
        is_active=True
    ).order_by('-prescription_date')[:5]

    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'recent_records': recent_records,
        'recent_prescriptions': recent_prescriptions,
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def profile(request):
    """我的档案 | My Profile"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    context = {
        'patient': patient,
    }
    return render(request, 'portal/profile.html', context)


@login_required
def profile_edit(request):
    """编辑档案 | Edit Profile"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    if request.method == 'POST':
        # 更新基本信息
        patient.phone = request.POST.get('phone', patient.phone)
        patient.email = request.POST.get('email', patient.email)
        patient.address = request.POST.get('address', patient.address)
        patient.emergency_contact_name = request.POST.get('emergency_contact_name', patient.emergency_contact_name)
        patient.emergency_contact_phone = request.POST.get('emergency_contact_phone', patient.emergency_contact_phone)
        patient.save()

        messages.success(request, _('档案已更新 | Profile updated successfully'))
        return redirect('portal:profile')

    context = {
        'patient': patient,
    }
    return render(request, 'portal/profile_edit.html', context)


@login_required
def records_list(request):
    """就诊记录列表 | Medical Records List"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    records = MedicalRecord.objects.filter(
        patient=patient,
        is_active=True
    ).order_by('-visit_date')

    context = {
        'patient': patient,
        'records': records,
    }
    return render(request, 'portal/records_list.html', context)


@login_required
def record_detail(request, pk):
    """就诊记录详情 | Medical Record Detail"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    record = get_object_or_404(MedicalRecord, pk=pk, patient=patient, is_active=True)

    context = {
        'patient': patient,
        'record': record,
    }
    return render(request, 'portal/record_detail.html', context)


@login_required
def prescriptions_list(request):
    """处方列表 | Prescriptions List"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    prescriptions = Prescription.objects.filter(
        patient=patient,
        is_active=True
    ).order_by('-prescription_date')

    context = {
        'patient': patient,
        'prescriptions': prescriptions,
    }
    return render(request, 'portal/prescriptions_list.html', context)


@login_required
def prescription_detail(request, pk):
    """处方详情 | Prescription Detail"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    prescription = get_object_or_404(Prescription, pk=pk, patient=patient, is_active=True)

    context = {
        'patient': patient,
        'prescription': prescription,
    }
    return render(request, 'portal/prescription_detail.html', context)


@login_required
def prescription_print(request, pk):
    """打印处方 | Print Prescription"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    prescription = get_object_or_404(Prescription, pk=pk, patient=patient, is_active=True)

    context = {
        'patient': patient,
        'prescription': prescription,
    }
    return render(request, 'portal/prescription_print.html', context)


@login_required
def appointments_list(request):
    """预约列表 | Appointments List"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    # 分为即将到来和历史预约
    upcoming = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=timezone.now().date(),
        is_active=True
    ).order_by('appointment_date', 'appointment_time')

    past = Appointment.objects.filter(
        patient=patient,
        appointment_date__lt=timezone.now().date(),
        is_active=True
    ).order_by('-appointment_date', '-appointment_time')

    context = {
        'patient': patient,
        'upcoming_appointments': upcoming,
        'past_appointments': past,
    }
    return render(request, 'portal/appointments_list.html', context)


@login_required
def appointment_detail(request, pk):
    """预约详情 | Appointment Detail"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    appointment = get_object_or_404(Appointment, pk=pk, patient=patient, is_active=True)

    context = {
        'patient': patient,
        'appointment': appointment,
    }
    return render(request, 'portal/appointment_detail.html', context)


@login_required
def appointment_cancel(request, pk):
    """取消预约 | Cancel Appointment"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    appointment = get_object_or_404(Appointment, pk=pk, patient=patient, is_active=True)

    if request.method == 'POST':
        if appointment.can_cancel():
            appointment.cancel(
                user=request.user,
                reason=request.POST.get('reason', '患者取消 | Cancelled by patient')
            )
            messages.success(request, _('预约已取消 | Appointment cancelled successfully'))
        else:
            messages.error(request, _('该预约无法取消 | This appointment cannot be cancelled'))

        return redirect('portal:appointments_list')

    context = {
        'patient': patient,
        'appointment': appointment,
    }
    return render(request, 'portal/appointment_cancel.html', context)


@login_required
def health_records(request):
    """健康档案 | Health Records"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    context = {
        'patient': patient,
    }
    return render(request, 'portal/health_records.html', context)


@login_required
def acupuncture_sessions(request):
    """针灸记录 | Acupuncture Sessions"""
    patient = get_patient_or_403(request)
    if not patient:
        return redirect('portal:dashboard')

    sessions = AcupunctureSession.objects.filter(
        patient=patient,
        is_active=True
    ).order_by('-session_date')

    context = {
        'patient': patient,
        'sessions': sessions,
    }
    return render(request, 'portal/acupuncture_sessions.html', context)
