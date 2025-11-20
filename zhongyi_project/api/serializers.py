"""Serializers for API endpoints."""
from rest_framework import serializers
from accounts.models import User
from patients.models import Patient, MedicalRecord
from prescriptions.models import (
    HerbCategory, Herb, ClassicFormula, FormulaHerb,
    Prescription, PrescriptionItem
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'license_number', 'specialization',
            'clinic_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class PatientListSerializer(serializers.ModelSerializer):
    """Serializer for patient list view."""

    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    assigned_practitioner_name = serializers.CharField(
        source='assigned_practitioner.get_full_name',
        read_only=True
    )

    class Meta:
        model = Patient
        fields = (
            'id', 'patient_id', 'full_name', 'chinese_name',
            'ic_number', 'phone', 'gender', 'age',
            'assigned_practitioner_name', 'is_active', 'updated_at'
        )


class PatientDetailSerializer(serializers.ModelSerializer):
    """Serializer for patient detail view."""

    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    assigned_practitioner = UserSerializer(read_only=True)
    assigned_practitioner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='practitioner'),
        source='assigned_practitioner',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Patient
        fields = (
            'id', 'patient_id', 'first_name', 'last_name', 'chinese_name',
            'full_name', 'ic_number', 'date_of_birth', 'gender', 'age',
            'blood_type', 'phone', 'email', 'address',
            'emergency_contact_name', 'emergency_contact_phone',
            'allergies', 'chronic_conditions', 'current_medications',
            'medical_history', 'family_history', 'tcm_constitution',
            'notes', 'assigned_practitioner', 'assigned_practitioner_id',
            'consent_data_sharing', 'consent_date',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'patient_id', 'created_at', 'updated_at')


class MedicalRecordSerializer(serializers.ModelSerializer):
    """Serializer for medical records."""

    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    practitioner_name = serializers.CharField(
        source='practitioner.get_full_name',
        read_only=True
    )
    record_type_display = serializers.CharField(
        source='get_record_type_display',
        read_only=True
    )

    class Meta:
        model = MedicalRecord
        fields = (
            'id', 'patient', 'patient_name', 'practitioner', 'practitioner_name',
            'record_type', 'record_type_display', 'visit_date',
            'chief_complaint', 'inspection_notes', 'tongue_diagnosis',
            'auscultation_notes', 'inquiry_notes', 'pulse_diagnosis',
            'palpation_notes', 'tcm_diagnosis', 'western_diagnosis',
            'treatment_principle', 'prescription', 'acupuncture_points',
            'other_treatments', 'lifestyle_advice', 'dietary_advice',
            'follow_up_notes', 'next_appointment',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


# ============================================================================
# Prescription & Herb Serializers
# ============================================================================

class HerbCategorySerializer(serializers.ModelSerializer):
    """Serializer for herb categories."""

    class Meta:
        model = HerbCategory
        fields = ('id', 'name_cn', 'name_en', 'description')


class HerbListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for herb listings."""

    category_name = serializers.CharField(source='category.name_cn', read_only=True)
    dosage_range = serializers.CharField(read_only=True)

    class Meta:
        model = Herb
        fields = (
            'id', 'code', 'name_cn', 'name_en', 'name_pinyin',
            'category_name', 'nature', 'dosage_range',
            'price_per_gram', 'is_active', 'is_toxic'
        )


class HerbDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for herb information."""

    category = HerbCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=HerbCategory.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    dosage_range = serializers.CharField(read_only=True)

    class Meta:
        model = Herb
        fields = (
            'id', 'code', 'name_cn', 'name_en', 'name_pinyin', 'name_latin',
            'category', 'category_id', 'nature', 'taste', 'meridians',
            'functions', 'indications', 'contraindications',
            'dosage_min', 'dosage_max', 'dosage_unit', 'dosage_range',
            'preparation_notes', 'price_per_gram',
            'is_active', 'is_toxic', 'requires_processing',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class FormulaHerbSerializer(serializers.ModelSerializer):
    """Serializer for herbs in a formula."""

    herb = HerbListSerializer(read_only=True)
    herb_id = serializers.PrimaryKeyRelatedField(
        queryset=Herb.objects.all(),
        source='herb',
        write_only=True
    )

    class Meta:
        model = FormulaHerb
        fields = ('id', 'herb', 'herb_id', 'role', 'dosage', 'notes')


class ClassicFormulaListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for formula listings."""

    class Meta:
        model = ClassicFormula
        fields = (
            'id', 'code', 'name_cn', 'name_en', 'name_pinyin',
            'source', 'functions', 'is_active'
        )


class ClassicFormulaDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for classic formulas."""

    formula_herbs = FormulaHerbSerializer(many=True, read_only=True)

    class Meta:
        model = ClassicFormula
        fields = (
            'id', 'code', 'name_cn', 'name_en', 'name_pinyin',
            'source', 'composition', 'functions', 'indications',
            'contraindications', 'modifications', 'is_active',
            'formula_herbs'
        )


class PrescriptionItemSerializer(serializers.ModelSerializer):
    """Serializer for prescription items."""

    herb = HerbListSerializer(read_only=True)
    herb_id = serializers.PrimaryKeyRelatedField(
        queryset=Herb.objects.all(),
        source='herb',
        write_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = PrescriptionItem
        fields = (
            'id', 'herb', 'herb_id', 'dosage', 'preparation',
            'notes', 'sequence', 'subtotal'
        )


class PrescriptionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for prescription listings."""

    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    practitioner_name = serializers.CharField(
        source='practitioner.get_full_name',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Prescription
        fields = (
            'id', 'prescription_number', 'prescription_date',
            'patient', 'patient_name', 'practitioner', 'practitioner_name',
            'status', 'status_display', 'doses', 'total_price'
        )


class PrescriptionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for prescriptions."""

    patient = PatientListSerializer(read_only=True)
    practitioner = UserSerializer(read_only=True)
    based_on_formula = ClassicFormulaListSerializer(read_only=True)
    items = PrescriptionItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Prescription
        fields = (
            'id', 'prescription_number', 'prescription_date',
            'patient', 'practitioner', 'diagnosis_session', 'based_on_formula',
            'diagnosis', 'treatment_principle', 'doses', 'decoction_method',
            'dietary_advice', 'lifestyle_advice', 'notes',
            'status', 'status_display', 'total_price',
            'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'prescription_number', 'prescription_date', 'created_at', 'updated_at')


class PrescriptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating prescriptions."""

    items = PrescriptionItemSerializer(many=True, required=False)

    class Meta:
        model = Prescription
        fields = (
            'patient', 'diagnosis_session', 'based_on_formula',
            'diagnosis', 'treatment_principle', 'doses', 'decoction_method',
            'dietary_advice', 'lifestyle_advice', 'notes', 'items'
        )

    def create(self, validated_data):
        """Create prescription with items."""
        items_data = validated_data.pop('items', [])
        prescription = Prescription.objects.create(**validated_data)

        for item_data in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)

        # Calculate total price
        prescription.calculate_total()
        prescription.save()

        return prescription
