"""
Export utilities for prescriptions (PDF and Excel).
处方导出工具 (PDF 和 Excel)
"""

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.utils import timezone
import os


# Register Chinese fonts for PDF (if available)
def register_chinese_fonts():
    """Register Chinese fonts for ReportLab."""
    try:
        # Try to register common Chinese fonts on Windows
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',  # Microsoft YaHei
            'C:/Windows/Fonts/simsun.ttc',  # SimSun
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    return 'ChineseFont'
                except:
                    continue
    except:
        pass
    return 'Helvetica'  # Fallback to default


class PrescriptionPDFExporter:
    """Export prescription to PDF format."""

    def __init__(self, prescription):
        self.prescription = prescription
        self.font_name = register_chinese_fonts()

    def generate(self):
        """Generate PDF and return BytesIO buffer."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        # Container for the 'Flowable' objects
        elements = []

        # Create custom styles
        styles = self._create_styles()

        # Header
        elements.append(Paragraph("中医处方 | TCM Prescription", styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*cm))

        # Clinic/Practice Information
        clinic_info = f"""
        <b>诊所信息 | Clinic Information</b><br/>
        Zhongyi TCM Clinic<br/>
        中医诊所
        """
        elements.append(Paragraph(clinic_info, styles['Normal']))
        elements.append(Spacer(1, 0.3*cm))

        # Prescription Information
        prescription_info = f"""
        <b>处方编号 | Prescription No.:</b> {self.prescription.prescription_number}<br/>
        <b>处方日期 | Date:</b> {self.prescription.prescription_date.strftime('%Y-%m-%d')}<br/>
        """
        elements.append(Paragraph(prescription_info, styles['Normal']))
        elements.append(Spacer(1, 0.3*cm))

        # Patient Information
        patient_info = f"""
        <b>患者信息 | Patient Information</b><br/>
        <b>姓名 | Name:</b> {self.prescription.patient.full_name}<br/>
        <b>中文名 | Chinese Name:</b> {self.prescription.patient.chinese_name or 'N/A'}<br/>
        <b>性别 | Gender:</b> {self.prescription.patient.get_gender_display()}<br/>
        <b>年龄 | Age:</b> {self.prescription.patient.age}<br/>
        <b>IC号 | IC No.:</b> {self.prescription.patient.ic_number}
        """
        elements.append(Paragraph(patient_info, styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))

        # Diagnosis
        if self.prescription.diagnosis:
            elements.append(Paragraph("<b>诊断 | Diagnosis:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.prescription.diagnosis, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Treatment Principle
        if self.prescription.treatment_principle:
            elements.append(Paragraph("<b>治则治法 | Treatment Principle:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.prescription.treatment_principle, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Herbs Table
        elements.append(Paragraph("<b>处方药物 | Prescription Herbs:</b>", styles['CustomHeading2']))
        elements.append(Spacer(1, 0.2*cm))

        # Create herbs table
        herbs_data = [['序号\nNo.', '药材\nHerb', '剂量(克)\nDosage(g)', '炮制\nPreparation']]
        for idx, item in enumerate(self.prescription.items.all(), 1):
            herbs_data.append([
                str(idx),
                f"{item.herb.name_cn}\n{item.herb.name_en}",
                str(item.dosage),
                item.preparation or '-'
            ])

        herbs_table = Table(herbs_data, colWidths=[1.5*cm, 8*cm, 3*cm, 4*cm])
        herbs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        elements.append(herbs_table)
        elements.append(Spacer(1, 0.5*cm))

        # Patent Medicines
        if self.prescription.patent_medicine_items.exists():
            elements.append(Paragraph("<b>中成药 | Patent Medicines:</b>", styles['CustomHeading2']))
            elements.append(Spacer(1, 0.2*cm))

            patent_data = [['序号\nNo.', '中成药\nMedicine', '数量\nQuantity', '用法\nUsage']]
            for idx, item in enumerate(self.prescription.patent_medicine_items.all(), 1):
                patent_data.append([
                    str(idx),
                    f"{item.medicine.name_cn}\n{item.medicine.name_en or ''}",
                    f"{item.quantity} 盒",
                    item.dosage_instruction or item.medicine.dosage_adult
                ])

            patent_table = Table(patent_data, colWidths=[1.5*cm, 6*cm, 3*cm, 6*cm])
            patent_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), self.font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            elements.append(patent_table)
            elements.append(Spacer(1, 0.5*cm))

        # Dosage Info
        dosage_info = f"""
        <b>剂数 | Doses:</b> {self.prescription.doses} 剂<br/>
        <b>煎煮方法 | Decoction Method:</b><br/>
        {self.prescription.decoction_method}
        """
        elements.append(Paragraph(dosage_info, styles['Normal']))
        elements.append(Spacer(1, 0.3*cm))

        # Dietary Advice
        if self.prescription.dietary_advice:
            elements.append(Paragraph("<b>饮食宜忌 | Dietary Advice:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.prescription.dietary_advice, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Lifestyle Advice
        if self.prescription.lifestyle_advice:
            elements.append(Paragraph("<b>生活建议 | Lifestyle Advice:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.prescription.lifestyle_advice, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Notes
        if self.prescription.notes:
            elements.append(Paragraph("<b>备注 | Notes:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.prescription.notes, styles['Normal']))
            elements.append(Spacer(1, 0.5*cm))

        # Practitioner Signature
        elements.append(Spacer(1, 1*cm))
        practitioner_name = self.prescription.practitioner.get_full_name() if self.prescription.practitioner else 'N/A'
        signature = f"""
        <b>医师签名 | Practitioner Signature:</b><br/>
        <br/>
        _______________________________<br/>
        {practitioner_name}<br/>
        {self.prescription.prescription_date.strftime('%Y-%m-%d')}
        """
        elements.append(Paragraph(signature, styles['Normal']))

        # Build PDF
        doc.build(elements)

        # Get PDF from buffer
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    def _create_styles(self):
        """Create custom paragraph styles."""
        styles = getSampleStyleSheet()

        # Custom Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName=self.font_name
        ))

        # Custom Heading2 style
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=6,
            fontName=self.font_name
        ))

        # Normal style
        styles['Normal'].fontName = self.font_name
        styles['Normal'].fontSize = 10
        styles['Normal'].leading = 14

        return styles


class PatientDataExcelExporter:
    """Export patient data to Excel format."""

    def __init__(self, patients):
        self.patients = patients

    def generate(self):
        """Generate Excel file and return BytesIO buffer."""
        wb = Workbook()
        ws = wb.active
        ws.title = "患者数据 | Patient Data"

        # Define header style
        header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Define border
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Headers
        headers = [
            '患者编号\nPatient ID',
            '姓名\nName',
            '中文名\nChinese Name',
            'IC号\nIC Number',
            '性别\nGender',
            '出生日期\nDate of Birth',
            '年龄\nAge',
            '电话\nPhone',
            '邮箱\nEmail',
            '血型\nBlood Type',
            '过敏史\nAllergies',
            '慢性疾病\nChronic Conditions',
            '中医体质\nTCM Constitution',
            '状态\nStatus',
            '创建日期\nCreated Date'
        ]

        # Write headers
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = thin_border

        # Set column widths
        column_widths = [15, 20, 15, 15, 10, 12, 8, 15, 25, 10, 30, 30, 15, 10, 12]
        for col_num, width in enumerate(column_widths, 1):
            ws.column_dimensions[chr(64 + col_num)].width = width

        # Write data
        for row_num, patient in enumerate(self.patients, 2):
            data = [
                str(patient.patient_id),
                patient.full_name,
                patient.chinese_name or '',
                patient.ic_number,
                patient.get_gender_display(),
                patient.date_of_birth.strftime('%Y-%m-%d'),
                patient.age,
                patient.phone,
                patient.email or '',
                patient.get_blood_type_display(),
                patient.allergies or '',
                patient.chronic_conditions or '',
                patient.tcm_constitution or '',
                '活跃 | Active' if patient.is_active else '非活跃 | Inactive',
                patient.created_at.strftime('%Y-%m-%d %H:%M')
            ]

            for col_num, value in enumerate(data, 1):
                cell = ws.cell(row=row_num, column=col_num)
                cell.value = value
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center", wrap_text=True)

        # Freeze header row
        ws.freeze_panes = 'A2'

        # Save to buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer.getvalue()


class MedicalRecordPDFExporter:
    """Export medical record to PDF format."""

    def __init__(self, medical_record):
        self.record = medical_record
        self.font_name = register_chinese_fonts()

    def generate(self):
        """Generate PDF and return BytesIO buffer."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        elements = []
        styles = self._create_styles()

        # Header
        elements.append(Paragraph("医疗记录 | Medical Record", styles['Title']))
        elements.append(Spacer(1, 0.5*cm))

        # Patient Information
        patient_info = f"""
        <b>患者信息 | Patient Information</b><br/>
        <b>姓名 | Name:</b> {self.record.patient.full_name}<br/>
        <b>中文名 | Chinese Name:</b> {self.record.patient.chinese_name or 'N/A'}<br/>
        <b>性别 | Gender:</b> {self.record.patient.get_gender_display()}<br/>
        <b>年龄 | Age:</b> {self.record.patient.age}<br/>
        <b>IC号 | IC No.:</b> {self.record.patient.ic_number}
        """
        elements.append(Paragraph(patient_info, styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))

        # Record Information
        record_info = f"""
        <b>记录类型 | Record Type:</b> {self.record.get_record_type_display()}<br/>
        <b>就诊日期 | Visit Date:</b> {self.record.visit_date.strftime('%Y-%m-%d %H:%M')}<br/>
        <b>医师 | Practitioner:</b> {self.record.practitioner.get_full_name() if self.record.practitioner else 'N/A'}
        """
        elements.append(Paragraph(record_info, styles['Normal']))
        elements.append(Spacer(1, 0.5*cm))

        # Chief Complaint
        elements.append(Paragraph("<b>主诉 | Chief Complaint:</b>", styles['CustomHeading2']))
        elements.append(Paragraph(self.record.chief_complaint, styles['Normal']))
        elements.append(Spacer(1, 0.3*cm))

        # Four Examinations
        elements.append(Paragraph("<b>四诊 | Four Examinations:</b>", styles['CustomHeading2']))

        if self.record.inspection_notes:
            elements.append(Paragraph("<i>望诊 | Inspection:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.inspection_notes, styles['Normal']))
            elements.append(Spacer(1, 0.2*cm))

        if self.record.tongue_diagnosis:
            elements.append(Paragraph("<i>舌诊 | Tongue Diagnosis:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.tongue_diagnosis, styles['Normal']))
            elements.append(Spacer(1, 0.2*cm))

        if self.record.auscultation_notes:
            elements.append(Paragraph("<i>闻诊 | Auscultation/Olfaction:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.auscultation_notes, styles['Normal']))
            elements.append(Spacer(1, 0.2*cm))

        if self.record.inquiry_notes:
            elements.append(Paragraph("<i>问诊 | Inquiry:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.inquiry_notes, styles['Normal']))
            elements.append(Spacer(1, 0.2*cm))

        if self.record.pulse_diagnosis:
            elements.append(Paragraph("<i>脉诊 | Pulse Diagnosis:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.pulse_diagnosis, styles['Normal']))
            elements.append(Spacer(1, 0.2*cm))

        if self.record.palpation_notes:
            elements.append(Paragraph("<i>切诊 | Palpation:</i>", styles['Normal']))
            elements.append(Paragraph(self.record.palpation_notes, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Diagnosis
        if self.record.tcm_diagnosis:
            elements.append(Paragraph("<b>中医诊断 | TCM Diagnosis:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.tcm_diagnosis, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.western_diagnosis:
            elements.append(Paragraph("<b>西医诊断 | Western Diagnosis:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.western_diagnosis, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Treatment
        if self.record.treatment_principle:
            elements.append(Paragraph("<b>治则治法 | Treatment Principle:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.treatment_principle, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.prescription:
            elements.append(Paragraph("<b>处方 | Prescription:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.prescription, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.acupuncture_points:
            elements.append(Paragraph("<b>针灸穴位 | Acupuncture Points:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.acupuncture_points, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.other_treatments:
            elements.append(Paragraph("<b>其他治疗 | Other Treatments:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.other_treatments, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        # Recommendations
        if self.record.lifestyle_advice:
            elements.append(Paragraph("<b>生活建议 | Lifestyle Advice:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.lifestyle_advice, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.dietary_advice:
            elements.append(Paragraph("<b>饮食建议 | Dietary Advice:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.dietary_advice, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.follow_up_notes:
            elements.append(Paragraph("<b>随访备注 | Follow-up Notes:</b>", styles['CustomHeading2']))
            elements.append(Paragraph(self.record.follow_up_notes, styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))

        if self.record.next_appointment:
            elements.append(Paragraph(
                f"<b>下次预约 | Next Appointment:</b> {self.record.next_appointment.strftime('%Y-%m-%d %H:%M')}",
                styles['Normal']
            ))

        # Build PDF
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    def _create_styles(self):
        """Create custom paragraph styles."""
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName=self.font_name
        ))

        styles.add(ParagraphStyle(
            name='Heading2',
            parent=styles['CustomHeading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=6,
            fontName=self.font_name
        ))

        styles['Normal'].fontName = self.font_name
        styles['Normal'].fontSize = 10
        styles['Normal'].leading = 14

        return styles
