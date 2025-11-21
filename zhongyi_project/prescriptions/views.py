"""Views for Prescription System."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal

from patients.models import Patient
from .models import (
    Herb, HerbCategory, ClassicFormula,
    Prescription, PrescriptionItem, PatentMedicine
)


class PractitionerRequiredMixin(UserPassesTestMixin):
    """Mixin to require practitioner or admin role."""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.role in ['practitioner', 'admin'] or
            self.request.user.is_staff
        )


class PrescriptionListView(LoginRequiredMixin, PractitionerRequiredMixin, ListView):
    """List all prescriptions."""
    model = Prescription
    template_name = 'prescriptions/prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 20

    def get_queryset(self):
        queryset = Prescription.objects.select_related('patient', 'practitioner')

        # Filter by practitioner for non-admin users
        if self.request.user.role == 'practitioner' and not self.request.user.is_staff:
            queryset = queryset.filter(practitioner=self.request.user)

        return queryset.order_by('-prescription_date')


class PrescriptionDetailView(LoginRequiredMixin, PractitionerRequiredMixin, DetailView):
    """View prescription details."""
    model = Prescription
    template_name = 'prescriptions/prescription_detail.html'
    context_object_name = 'prescription'


@login_required
def select_patient_for_prescription(request):
    """Select a patient to create a prescription."""
    patients = Patient.objects.filter(is_active=True).order_by('last_name', 'first_name')

    return render(request, 'prescriptions/select_patient.html', {
        'patients': patients,
    })


@login_required
def create_prescription(request, patient_pk):
    """Create a new prescription for a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    herbs = Herb.objects.filter(is_active=True).order_by('name_pinyin', 'name_cn')
    categories = HerbCategory.objects.all()
    patent_medicines = PatentMedicine.objects.filter(is_active=True).order_by('name_cn')

    if request.method == 'POST':
        # Create prescription
        prescription = Prescription.objects.create(
            patient=patient,
            practitioner=request.user,
            diagnosis=request.POST.get('diagnosis', ''),
            treatment_principle=request.POST.get('treatment_principle', ''),
            doses=int(request.POST.get('doses', 7)),
            decoction_method=request.POST.get('decoction_method', '水煎服，每日一剂，分两次温服。'),
            dietary_advice=request.POST.get('dietary_advice', ''),
            lifestyle_advice=request.POST.get('lifestyle_advice', ''),
            notes=request.POST.get('notes', ''),
        )

        # Add herbs
        herb_ids = request.POST.getlist('herb_id')
        dosages = request.POST.getlist('dosage')
        preparations = request.POST.getlist('preparation')

        for i, herb_id in enumerate(herb_ids):
            if herb_id and dosages[i]:
                try:
                    herb = Herb.objects.get(pk=herb_id)
                    PrescriptionItem.objects.create(
                        prescription=prescription,
                        herb=herb,
                        dosage=Decimal(dosages[i]),
                        preparation=preparations[i] if i < len(preparations) else '',
                        sequence=i,
                    )
                except (Herb.DoesNotExist, ValueError):
                    pass

        # Add patent medicines
        from .models import PrescriptionPatentMedicine
        patent_medicine_ids = request.POST.getlist('patent_medicine_id')
        patent_quantities = request.POST.getlist('patent_quantity')
        patent_usages = request.POST.getlist('patent_usage_instructions')

        for i, medicine_id in enumerate(patent_medicine_ids):
            if medicine_id and patent_quantities[i]:
                try:
                    medicine = PatentMedicine.objects.get(pk=medicine_id)
                    quantity = int(patent_quantities[i])
                    usage = patent_usages[i] if i < len(patent_usages) else medicine.dosage_adult

                    PrescriptionPatentMedicine.objects.create(
                        prescription=prescription,
                        medicine=medicine,
                        quantity=quantity,
                        dosage_instruction=usage,
                    )
                except (PatentMedicine.DoesNotExist, ValueError):
                    pass

        # Calculate total
        prescription.calculate_total()
        prescription.save()

        messages.success(request, _('处方已创建！| Prescription created successfully!'))
        return redirect('prescriptions:detail', pk=prescription.pk)

    return render(request, 'prescriptions/create_prescription.html', {
        'patient': patient,
        'herbs': herbs,
        'categories': categories,
        'patent_medicines': patent_medicines,
    })


@login_required
def edit_prescription(request, pk):
    """Edit an existing prescription."""
    prescription = get_object_or_404(Prescription, pk=pk)

    # Check permission
    if not (request.user.is_staff or request.user.role == 'admin' or prescription.practitioner == request.user):
        messages.error(request, _('您没有权限编辑此处方。| You do not have permission to edit this prescription.'))
        return redirect('prescriptions:detail', pk=pk)

    herbs = Herb.objects.filter(is_active=True).order_by('name_pinyin', 'name_cn')
    categories = HerbCategory.objects.all()
    patent_medicines = PatentMedicine.objects.filter(is_active=True).order_by('name_cn')

    if request.method == 'POST':
        # Update prescription info
        prescription.diagnosis = request.POST.get('diagnosis', '')
        prescription.treatment_principle = request.POST.get('treatment_principle', '')
        prescription.doses = int(request.POST.get('doses', 7))
        prescription.decoction_method = request.POST.get('decoction_method', '')
        prescription.dietary_advice = request.POST.get('dietary_advice', '')
        prescription.lifestyle_advice = request.POST.get('lifestyle_advice', '')
        prescription.notes = request.POST.get('notes', '')

        # Clear existing items and re-add
        prescription.items.all().delete()
        prescription.patent_medicine_items.all().delete()

        # Add herbs
        herb_ids = request.POST.getlist('herb_id')
        dosages = request.POST.getlist('dosage')
        preparations = request.POST.getlist('preparation')

        for i, herb_id in enumerate(herb_ids):
            if herb_id and dosages[i]:
                try:
                    herb = Herb.objects.get(pk=herb_id)
                    PrescriptionItem.objects.create(
                        prescription=prescription,
                        herb=herb,
                        dosage=Decimal(dosages[i]),
                        preparation=preparations[i] if i < len(preparations) else '',
                        sequence=i,
                    )
                except (Herb.DoesNotExist, ValueError):
                    pass

        # Add patent medicines
        from .models import PrescriptionPatentMedicine
        patent_medicine_ids = request.POST.getlist('patent_medicine_id')
        patent_quantities = request.POST.getlist('patent_quantity')
        patent_usages = request.POST.getlist('patent_usage_instructions')

        for i, medicine_id in enumerate(patent_medicine_ids):
            if medicine_id and patent_quantities[i]:
                try:
                    medicine = PatentMedicine.objects.get(pk=medicine_id)
                    quantity = int(patent_quantities[i])
                    usage = patent_usages[i] if i < len(patent_usages) else medicine.dosage_adult

                    PrescriptionPatentMedicine.objects.create(
                        prescription=prescription,
                        medicine=medicine,
                        quantity=quantity,
                        dosage_instruction=usage,
                    )
                except (PatentMedicine.DoesNotExist, ValueError):
                    pass

        # Recalculate total
        prescription.calculate_total()
        prescription.save()

        messages.success(request, _('处方已更新！| Prescription updated successfully!'))
        return redirect('prescriptions:detail', pk=pk)

    return render(request, 'prescriptions/edit_prescription.html', {
        'prescription': prescription,
        'patient': prescription.patient,
        'herbs': herbs,
        'categories': categories,
        'patent_medicines': patent_medicines,
    })


@login_required
def delete_prescription(request, pk):
    """Delete a prescription (admin/staff only)."""
    prescription = get_object_or_404(Prescription, pk=pk)
    patient_pk = prescription.patient.pk

    # Check permission
    if not (request.user.is_staff or request.user.role == 'admin'):
        messages.error(request, _('您没有权限删除此处方。| You do not have permission to delete this prescription.'))
        return redirect('prescriptions:detail', pk=pk)

    if request.method == 'POST':
        prescription.delete()
        messages.success(request, _('处方已删除！| Prescription deleted successfully!'))
        return redirect('patients:detail', pk=patient_pk)

    return render(request, 'prescriptions/confirm_delete.html', {
        'prescription': prescription,
    })


@login_required
def print_prescription(request, pk):
    """Print-friendly prescription view."""
    prescription = get_object_or_404(Prescription, pk=pk)

    return render(request, 'prescriptions/print_prescription.html', {
        'prescription': prescription,
    })


class HerbListView(LoginRequiredMixin, ListView):
    """List all herbs."""
    model = Herb
    template_name = 'prescriptions/herb_list.html'
    context_object_name = 'herbs'
    paginate_by = 50

    def get_queryset(self):
        queryset = Herb.objects.filter(is_active=True)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name_cn__icontains=search) |
                Q(name_en__icontains=search) |
                Q(name_pinyin__icontains=search)
            )

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by nature
        nature = self.request.GET.get('nature')
        if nature:
            queryset = queryset.filter(nature=nature)

        return queryset.order_by('name_pinyin', 'name_cn')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HerbCategory.objects.all()
        context['natures'] = Herb.Nature.choices
        return context


class HerbDetailView(LoginRequiredMixin, DetailView):
    """View herb details."""
    model = Herb
    template_name = 'prescriptions/herb_detail.html'
    context_object_name = 'herb'


class FormulaListView(LoginRequiredMixin, ListView):
    """List all classic formulas."""
    model = ClassicFormula
    template_name = 'prescriptions/formula_list.html'
    context_object_name = 'formulas'
    paginate_by = 20

    def get_queryset(self):
        queryset = ClassicFormula.objects.filter(is_active=True)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name_cn__icontains=search) |
                Q(name_en__icontains=search) |
                Q(name_pinyin__icontains=search)
            )

        return queryset.order_by('name_pinyin', 'name_cn')


class FormulaDetailView(LoginRequiredMixin, DetailView):
    """View formula details."""
    model = ClassicFormula
    template_name = 'prescriptions/formula_detail.html'
    context_object_name = 'formula'


@login_required
def api_herb_search(request):
    """API endpoint for herb search (AJAX)."""
    query = request.GET.get('q', '')

    if len(query) < 1:
        return JsonResponse({'results': []})

    herbs = Herb.objects.filter(
        is_active=True
    ).filter(
        Q(name_cn__icontains=query) |
        Q(name_en__icontains=query) |
        Q(name_pinyin__icontains=query)
    )[:20]

    results = []
    for herb in herbs:
        results.append({
            'id': herb.pk,
            'name_cn': herb.name_cn,
            'name_en': herb.name_en,
            'name_pinyin': herb.name_pinyin,
            'dosage_range': herb.dosage_range,
            'nature': herb.get_nature_display(),
        })

    return JsonResponse({'results': results})


@login_required
def api_ai_prescription_recommend(request):
    """
    API endpoint for AI prescription recommendations
    AI处方推荐API接口
    """
    from diagnosis.ai_assistant import TCMAIAssistant
    import json

    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)

    try:
        data = json.loads(request.body)
        syndrome_code = data.get('syndrome_code')
        patient_age = data.get('patient_age')
        patient_gender = data.get('patient_gender')

        if not syndrome_code:
            return JsonResponse({'error': 'syndrome_code is required'}, status=400)

        # Get AI recommendation
        ai_assistant = TCMAIAssistant()
        recommendation = ai_assistant.recommend_prescription(
            syndrome_code=syndrome_code,
            patient_age=patient_age,
            patient_gender=patient_gender,
        )

        return JsonResponse({
            'success': True,
            'recommendation': recommendation,
            'disclaimer': '⚠️ AI建议仅供参考，需要执业医师审核确认 | AI suggestions are for reference only and require practitioner review.',
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class PatentMedicineListView(LoginRequiredMixin, ListView):
    """List all patent medicines (中成药)."""
    model = PatentMedicine
    template_name = 'prescriptions/patentmedicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 20

    def get_queryset(self):
        queryset = PatentMedicine.objects.filter(is_active=True)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name_cn__icontains=search) |
                Q(name_en__icontains=search) |
                Q(manufacturer__icontains=search)
            )

        # Filter by dosage form
        dosage_form = self.request.GET.get('dosage_form')
        if dosage_form:
            queryset = queryset.filter(dosage_form=dosage_form)

        # Filter by prescription type
        prescription_type = self.request.GET.get('prescription_type')
        if prescription_type:
            queryset = queryset.filter(prescription_type=prescription_type)

        # Filter by stock status
        in_stock = self.request.GET.get('in_stock')
        if in_stock == '1':
            queryset = queryset.filter(is_in_stock=True)

        return queryset.order_by('name_cn')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dosage_forms'] = PatentMedicine.DosageForm.choices
        context['prescription_types'] = PatentMedicine.PrescriptionType.choices
        return context


class PatentMedicineDetailView(LoginRequiredMixin, DetailView):
    """View patent medicine details."""
    model = PatentMedicine
    template_name = 'prescriptions/patentmedicine_detail.html'
    context_object_name = 'medicine'
