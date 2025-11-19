"""Serializers for Diagnosis app REST API."""
from rest_framework import serializers
from .models import Symptom, Syndrome, DiagnosisSession, SyndromeSysmptomWeight


class SymptomSerializer(serializers.ModelSerializer):
    """Serializer for Symptom model."""

    class Meta:
        model = Symptom
        fields = ['id', 'code', 'name_en', 'name_cn', 'category', 'description']


class SyndromeSysmptomWeightSerializer(serializers.ModelSerializer):
    """Serializer for syndrome-symptom weights."""
    symptom = SymptomSerializer(read_only=True)

    class Meta:
        model = SyndromeSysmptomWeight
        fields = ['symptom', 'weight', 'is_primary']


class SyndromeSerializer(serializers.ModelSerializer):
    """Serializer for Syndrome model."""
    symptom_weights = SyndromeSysmptomWeightSerializer(
        source='syndromesysmptomweight_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Syndrome
        fields = [
            'id', 'code', 'name_en', 'name_cn', 'category',
            'description', 'etiology', 'clinical_manifestations',
            'tongue_signs', 'pulse_signs', 'treatment_principle',
            'symptom_weights'
        ]


class SyndromeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for syndrome listings."""

    class Meta:
        model = Syndrome
        fields = ['id', 'code', 'name_en', 'name_cn', 'category', 'treatment_principle']


class DiagnosisSessionSerializer(serializers.ModelSerializer):
    """Serializer for DiagnosisSession model."""
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    practitioner_name = serializers.CharField(source='practitioner.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DiagnosisSession
        fields = [
            'id', 'patient', 'patient_name', 'practitioner', 'practitioner_name',
            'chief_complaint', 'history_of_present_illness', 'past_medical_history',
            'tongue_body_color', 'tongue_coating', 'tongue_shape', 'tongue_moisture',
            'pulse_rate', 'pulse_rhythm', 'pulse_strength', 'pulse_quality',
            'inspection_notes', 'auscultation_notes', 'inquiry_notes', 'palpation_notes',
            'selected_symptoms', 'ai_suggested_syndromes', 'final_diagnosis',
            'treatment_principle', 'notes', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'ai_suggested_syndromes']


class DiagnosisSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating diagnosis sessions."""

    class Meta:
        model = DiagnosisSession
        fields = [
            'patient', 'chief_complaint', 'history_of_present_illness',
            'past_medical_history', 'selected_symptoms'
        ]


class SymptomAnalysisSerializer(serializers.Serializer):
    """Serializer for symptom analysis request."""
    symptom_codes = serializers.ListField(
        child=serializers.CharField(max_length=20),
        min_length=1
    )
    tongue_data = serializers.DictField(required=False, allow_null=True)
    pulse_data = serializers.DictField(required=False, allow_null=True)


class SyndromeMatchSerializer(serializers.Serializer):
    """Serializer for syndrome match results."""
    syndrome_id = serializers.IntegerField()
    syndrome_code = serializers.CharField()
    name_en = serializers.CharField()
    name_cn = serializers.CharField()
    confidence = serializers.FloatField()
    matched_symptoms = serializers.ListField(child=serializers.CharField())
    treatment_principle = serializers.CharField()
