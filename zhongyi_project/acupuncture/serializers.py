from rest_framework import serializers
from .models import AcupunctureSession


class AcupunctureSessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    assigned_practitioner_name = serializers.CharField(
        source='assigned_practitioner.get_full_name',
        read_only=True
    )
    treatment_type_display = serializers.CharField(
        source='get_treatment_type_display',
        read_only=True
    )

    class Meta:
        model = AcupunctureSession
        fields = [
            'id',
            'patient_name',
            'session_date',
            'treatment_type',
            'treatment_type_display',
            'assigned_practitioner_name',
            'created_at'
        ]


class AcupunctureSessionDetailSerializer(serializers.ModelSerializer):
    """Full serializer with all fields."""
    patient_id = serializers.PrimaryKeyRelatedField(
        source='patient',
        queryset=__import__('patients.models', fromlist=['Patient']).Patient.objects.filter(is_active=True),
        write_only=True,
        required=True
    )
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    assigned_practitioner_id = serializers.PrimaryKeyRelatedField(
        source='assigned_practitioner',
        queryset=__import__('django.contrib.auth', fromlist=['get_user_model']).get_user_model().objects.filter(role='practitioner'),
        write_only=True,
        required=False
    )
    assigned_practitioner_name = serializers.CharField(
        source='assigned_practitioner.get_full_name',
        read_only=True
    )
    treatment_type_display = serializers.CharField(
        source='get_treatment_type_display',
        read_only=True
    )
    needle_retention_time_display = serializers.CharField(
        source='get_needle_retention_time_display',
        read_only=True
    )
    patient_response_display = serializers.CharField(
        source='get_patient_response_display',
        read_only=True
    )

    class Meta:
        model = AcupunctureSession
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
