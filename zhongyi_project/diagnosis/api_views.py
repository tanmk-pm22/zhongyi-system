"""API ViewSets for Diagnosis app."""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Symptom, Syndrome, DiagnosisSession
from .serializers import (
    SymptomSerializer,
    SyndromeSerializer,
    SyndromeListSerializer,
    DiagnosisSessionSerializer,
    DiagnosisSessionCreateSerializer,
    SymptomAnalysisSerializer,
    SyndromeMatchSerializer,
)
from .analysis import analyze_symptoms


class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing symptoms."""
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Symptom.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of symptom categories."""
        categories = [
            {'value': choice[0], 'label_en': choice[1], 'label_cn': self._get_cn_label(choice[0])}
            for choice in Symptom.Category.choices
        ]
        return Response(categories)

    def _get_cn_label(self, category):
        """Get Chinese label for category."""
        labels = {
            'general': '全身',
            'head': '头面',
            'chest': '胸腹',
            'limbs': '四肢',
            'sleep': '睡眠',
            'appetite': '食欲',
            'urination': '二便',
            'emotion': '情志',
        }
        return labels.get(category, category)


class SyndromeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing syndromes."""
    queryset = Syndrome.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return SyndromeListSerializer
        return SyndromeSerializer

    def get_queryset(self):
        queryset = Syndrome.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of syndrome categories."""
        categories = [
            {'value': choice[0], 'label_en': choice[1], 'label_cn': self._get_cn_label(choice[0])}
            for choice in Syndrome.Category.choices
        ]
        return Response(categories)

    def _get_cn_label(self, category):
        """Get Chinese label for category."""
        labels = {
            'qi': '气',
            'blood': '血',
            'yin_yang': '阴阳',
            'organ': '脏腑',
            'fluid': '津液',
            'external': '外感',
        }
        return labels.get(category, category)


class DiagnosisSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for diagnosis sessions."""
    queryset = DiagnosisSession.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosisSessionCreateSerializer
        return DiagnosisSessionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = DiagnosisSession.objects.all()

        # Filter by user role
        if hasattr(user, 'is_practitioner') and user.is_practitioner:
            queryset = queryset.filter(practitioner=user)
        elif hasattr(user, 'patient_profile'):
            queryset = queryset.filter(patient=user.patient_profile)

        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(practitioner=self.request.user)

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """Run AI analysis on a diagnosis session."""
        session = self.get_object()

        # Prepare tongue data
        tongue_data = {
            'body_color': session.tongue_body_color,
            'coating': session.tongue_coating,
            'shape': session.tongue_shape,
            'moisture': session.tongue_moisture,
        }

        # Prepare pulse data
        pulse_data = {
            'rate': session.pulse_rate,
            'rhythm': session.pulse_rhythm,
            'strength': session.pulse_strength,
            'quality': session.pulse_quality,
        }

        # Run analysis
        results = analyze_symptoms(
            session.selected_symptoms,
            tongue_data,
            pulse_data
        )

        # Update session with results
        session.ai_suggested_syndromes = results
        session.save()

        return Response({
            'results': results,
            'session_id': session.id
        })

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a diagnosis session as completed."""
        session = self.get_object()
        final_diagnosis = request.data.get('final_diagnosis', '')
        treatment_principle = request.data.get('treatment_principle', '')

        session.final_diagnosis = final_diagnosis
        session.treatment_principle = treatment_principle
        session.status = 'completed'
        session.save()

        return Response(DiagnosisSessionSerializer(session).data)


class AnalysisViewSet(viewsets.ViewSet):
    """ViewSet for symptom analysis."""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def symptoms(self, request):
        """Analyze symptoms and return syndrome matches."""
        serializer = SymptomAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        symptom_codes = serializer.validated_data['symptom_codes']
        tongue_data = serializer.validated_data.get('tongue_data')
        pulse_data = serializer.validated_data.get('pulse_data')

        results = analyze_symptoms(symptom_codes, tongue_data, pulse_data)

        return Response({
            'results': results,
            'symptom_count': len(symptom_codes)
        })
