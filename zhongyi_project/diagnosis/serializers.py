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
    patient_name = serializers.SerializerMethodField()
    practitioner_name = serializers.CharField(source='practitioner.get_full_name', read_only=True)

    class Meta:
        model = DiagnosisSession
        fields = [
            'id', 'patient', 'patient_name', 'practitioner', 'practitioner_name',
            'session_date', 'chief_complaint',
            # Inspection (望诊)
            'spirit_status', 'complexion',
            'tongue_body_color', 'tongue_body_shape', 'tongue_coating_color',
            'tongue_coating_texture', 'tongue_notes',
            # Auscultation (闻诊)
            'voice_quality', 'breath_odor', 'auscultation_notes',
            # Inquiry (问诊)
            'selected_symptoms', 'symptom_details', 'sleep_quality', 'appetite',
            'thirst', 'defecation', 'urination', 'perspiration', 'inquiry_notes',
            # Palpation (切诊)
            'pulse_left_cun', 'pulse_left_guan', 'pulse_left_chi',
            'pulse_right_cun', 'pulse_right_guan', 'pulse_right_chi',
            'pulse_overall', 'palpation_notes',
            # Analysis & Diagnosis
            'ai_suggested_syndromes', 'final_diagnosis', 'treatment_principle', 'notes',
            'is_complete', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'ai_suggested_syndromes', 'session_date']

    def get_patient_name(self, obj):
        """Get patient's full name."""
        if obj.patient and obj.patient.user_account:
            return obj.patient.user_account.get_full_name()
        elif obj.patient:
            return f"{obj.patient.first_name} {obj.patient.last_name}"
        return ""


class DiagnosisSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating diagnosis sessions."""

    class Meta:
        model = DiagnosisSession
        fields = [
            'patient', 'chief_complaint', 'selected_symptoms',
            # Optional initial fields
            'spirit_status', 'complexion',
            'tongue_body_color', 'tongue_body_shape', 'tongue_coating_color',
            'tongue_coating_texture', 'tongue_notes',
            'voice_quality', 'breath_odor', 'auscultation_notes',
            'symptom_details', 'sleep_quality', 'appetite', 'thirst',
            'defecation', 'urination', 'perspiration', 'inquiry_notes',
            'pulse_left_cun', 'pulse_left_guan', 'pulse_left_chi',
            'pulse_right_cun', 'pulse_right_guan', 'pulse_right_chi',
            'pulse_overall', 'palpation_notes'
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
