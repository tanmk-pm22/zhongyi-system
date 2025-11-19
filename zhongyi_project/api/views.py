"""API views using Django REST Framework."""
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from accounts.models import User
from patients.models import Patient, MedicalRecord
from .serializers import (
    UserSerializer, PatientListSerializer, PatientDetailSerializer,
    MedicalRecordSerializer
)


class IsPractitionerOrAdmin(permissions.BasePermission):
    """Permission to check if user is practitioner or admin."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ['practitioner', 'admin'] or
            request.user.is_staff
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsPractitionerOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def practitioners(self, request):
        """Get all practitioners."""
        practitioners = User.objects.filter(role='practitioner')
        serializer = self.get_serializer(practitioners, many=True)
        return Response(serializer.data)


class PatientViewSet(viewsets.ModelViewSet):
    """API endpoint for patients CRUD operations."""
    queryset = Patient.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated, IsPractitionerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'chinese_name', 'ic_number', 'phone', 'email']
    ordering_fields = ['updated_at', 'created_at', 'last_name', 'first_name']
    ordering = ['-updated_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by assigned practitioner for non-admin/staff users
        user = self.request.user
        if user.role == 'practitioner' and not user.is_staff:
            queryset = queryset.filter(assigned_practitioner=user)

        return queryset.select_related('assigned_practitioner')

    def perform_create(self, serializer):
        # Auto-assign current practitioner if not specified
        if not serializer.validated_data.get('assigned_practitioner'):
            if self.request.user.role == 'practitioner':
                serializer.save(assigned_practitioner=self.request.user)
                return
        serializer.save()

    @action(detail=True, methods=['get'])
    def records(self, request, pk=None):
        """Get all medical records for a patient."""
        patient = self.get_object()
        records = patient.medical_records.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search patients by various fields."""
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])

        patients = self.get_queryset().filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(chinese_name__icontains=query) |
            Q(ic_number__icontains=query) |
            Q(phone__icontains=query)
        )[:20]

        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def qrcode_data(self, request, pk=None):
        """Get QR code data for a patient."""
        patient = self.get_object()
        return Response({
            'patient_id': str(patient.patient_id),
            'name': patient.full_name,
            'qrcode_url': request.build_absolute_uri(f'/patients/{patient.pk}/qrcode/')
        })


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """API endpoint for medical records."""
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsPractitionerOrAdmin]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['visit_date', 'created_at']
    ordering = ['-visit_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by patient if specified
        patient_id = self.request.query_params.get('patient')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        # Filter by practitioner for non-admin/staff users
        user = self.request.user
        if user.role == 'practitioner' and not user.is_staff:
            queryset = queryset.filter(
                Q(practitioner=user) |
                Q(patient__assigned_practitioner=user)
            )

        return queryset.select_related('patient', 'practitioner')

    def perform_create(self, serializer):
        serializer.save(practitioner=self.request.user)
