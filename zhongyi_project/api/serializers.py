"""Serializers for API endpoints."""
from rest_framework import serializers
from accounts.models import User
from patients.models import Patient, MedicalRecord


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
