from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Q

from .models import Appointment, TimeSlot, BlockedDate
from accounts.models import User
from patients.models import Patient


def booking_home(request):
    """预约首页 | Booking Home"""
    return redirect('booking:booking_step1')


def booking_step1_service(request):
    """第一步：选择服务 | Step 1: Select Service"""
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        request.session['booking_service_type'] = service_type
        return redirect('booking:booking_step2')

    context = {
        'service_choices': Appointment.SERVICE_TYPE_CHOICES,
    }
    return render(request, 'booking/step1_service.html', context)


def booking_step2_practitioner(request):
    """第二步：选择医师 | Step 2: Select Practitioner"""
    if request.method == 'POST':
        practitioner_id = request.POST.get('practitioner_id')
        if practitioner_id:
            request.session['booking_practitioner_id'] = int(practitioner_id)
        else:
            request.session['booking_practitioner_id'] = None
        return redirect('booking:booking_step3')

    practitioners = User.objects.filter(
        role='practitioner',
        is_active=True
    )

    context = {
        'practitioners': practitioners,
    }
    return render(request, 'booking/step2_practitioner.html', context)


def booking_step3_datetime(request):
    """第三步：选择日期时间 | Step 3: Select Date & Time"""
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        request.session['booking_date'] = appointment_date
        request.session['booking_time'] = appointment_time
        return redirect('booking:booking_step4')

    today = timezone.now().date()
    available_dates = [today + timedelta(days=i) for i in range(30)]

    context = {
        'available_dates': available_dates,
    }
    return render(request, 'booking/step3_datetime.html', context)


def booking_step4_info(request):
    """第四步：填写信息 | Step 4: Enter Information"""
    if request.method == 'POST':
        request.session['booking_name'] = request.POST.get('name')
        request.session['booking_phone'] = request.POST.get('phone')
        request.session['booking_email'] = request.POST.get('email', '')
        request.session['booking_chief_complaint'] = request.POST.get('chief_complaint', '')
        return redirect('booking:booking_confirm')

    patient = None
    if request.user.is_authenticated:
        try:
            patient = Patient.objects.get(user_account=request.user)
        except Patient.DoesNotExist:
            pass

    context = {
        'patient': patient,
    }
    return render(request, 'booking/step4_info.html', context)


def booking_confirm(request):
    """确认预约 | Confirm Booking"""
    if request.method == 'POST':
        try:
            service_type = request.session.get('booking_service_type')
            practitioner_id = request.session.get('booking_practitioner_id')
            appointment_date = request.session.get('booking_date')
            appointment_time = request.session.get('booking_time')
            name = request.session.get('booking_name')
            phone = request.session.get('booking_phone')
            email = request.session.get('booking_email', '')
            chief_complaint = request.session.get('booking_chief_complaint', '')

            practitioner = None
            if practitioner_id:
                practitioner = User.objects.get(pk=practitioner_id)

            patient = None
            if request.user.is_authenticated:
                try:
                    patient = Patient.objects.get(user_account=request.user)
                except Patient.DoesNotExist:
                    pass

            appointment = Appointment.objects.create(
                patient=patient,
                practitioner=practitioner,
                service_type=service_type,
                appointment_date=datetime.strptime(appointment_date, '%Y-%m-%d').date(),
                appointment_time=datetime.strptime(appointment_time, '%H:%M').time(),
                patient_name=name,
                patient_phone=phone,
                patient_email=email,
                chief_complaint=chief_complaint,
                status='pending',
            )

            for key in ['booking_service_type', 'booking_practitioner_id', 'booking_date',
                        'booking_time', 'booking_name', 'booking_phone', 'booking_email',
                        'booking_chief_complaint']:
                if key in request.session:
                    del request.session[key]

            return redirect('booking:booking_success', appointment_number=appointment.appointment_number)

        except Exception as e:
            messages.error(request, _('预约失败，请重试。| Booking failed, please try again.'))
            return redirect('booking:booking_step1')

    context = {
        'service_type': request.session.get('booking_service_type'),
        'practitioner_id': request.session.get('booking_practitioner_id'),
        'appointment_date': request.session.get('booking_date'),
        'appointment_time': request.session.get('booking_time'),
        'name': request.session.get('booking_name'),
        'phone': request.session.get('booking_phone'),
        'email': request.session.get('booking_email'),
        'chief_complaint': request.session.get('booking_chief_complaint'),
    }

    if context['practitioner_id']:
        try:
            context['practitioner'] = User.objects.get(pk=context['practitioner_id'])
        except User.DoesNotExist:
            pass

    return render(request, 'booking/confirm.html', context)


def booking_success(request, appointment_number):
    """预约成功 | Booking Success"""
    appointment = get_object_or_404(Appointment, appointment_number=appointment_number)
    context = {
        'appointment': appointment,
    }
    return render(request, 'booking/success.html', context)


def api_available_slots(request):
    """API: 获取可用时间段 | API: Get Available Slots"""
    date_str = request.GET.get('date')
    practitioner_id = request.GET.get('practitioner_id')

    if not date_str:
        return JsonResponse({'error': 'Date required'}, status=400)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    weekday = date.weekday()
    time_slots = TimeSlot.objects.filter(day_of_week=weekday, is_active=True)

    if practitioner_id:
        time_slots = time_slots.filter(
            Q(practitioner_id=practitioner_id) | Q(practitioner__isnull=True)
        )

    blocked = BlockedDate.objects.filter(
        blocked_date=date,
        is_active=True
    ).filter(
        Q(practitioner__isnull=True) |
        Q(practitioner_id=practitioner_id) if practitioner_id else Q()
    ).exists()

    if blocked:
        return JsonResponse({'slots': []})

    available_slots = []
    for slot in time_slots:
        available_slots.append({
            'time': slot.start_time.strftime('%H:%M'),
            'available': True,
        })

    return JsonResponse({'slots': available_slots})


def api_check_availability(request):
    """API: 检查可用性 | API: Check Availability"""
    return JsonResponse({'available': True})
