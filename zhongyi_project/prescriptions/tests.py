"""Tests for prescriptions app."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from patients.models import Patient
from .models import (
    HerbCategory, Herb, ClassicFormula, FormulaHerb,
    Prescription, PrescriptionItem
)

User = get_user_model()


class HerbCategoryModelTest(TestCase):
    """Test HerbCategory model."""

    def setUp(self):
        """Set up test data."""
        self.category = HerbCategory.objects.create(
            name_cn='补气药',
            name_en='Qi-Tonifying Herbs',
            description='Herbs that tonify Qi'
        )

    def test_category_creation(self):
        """Test herb category is created successfully."""
        self.assertEqual(self.category.name_cn, '补气药')
        self.assertEqual(self.category.name_en, 'Qi-Tonifying Herbs')

    def test_category_str(self):
        """Test category string representation."""
        expected = f"{self.category.name_cn} | {self.category.name_en}"
        self.assertEqual(str(self.category), expected)


class HerbModelTest(TestCase):
    """Test Herb model."""

    def setUp(self):
        """Set up test data."""
        self.category = HerbCategory.objects.create(
            name_cn='补气药',
            name_en='Qi-Tonifying Herbs'
        )

        self.herb = Herb.objects.create(
            code='H001',
            name_cn='人参',
            name_en='Ginseng',
            name_pinyin='Ren Shen',
            name_latin='Ginseng Radix et Rhizoma',
            category=self.category,
            nature='warm',
            taste=['sweet', 'bitter'],
            meridians=['spleen', 'lung', 'heart'],
            functions='大补元气，复脉固脱',
            indications='体虚欲脱，脾虚食少',
            contraindications='实证、热证忌用',
            dosage_min=Decimal('3.00'),
            dosage_max=Decimal('9.00'),
            price_per_gram=Decimal('2.50')
        )

    def test_herb_creation(self):
        """Test herb is created successfully."""
        self.assertEqual(self.herb.code, 'H001')
        self.assertEqual(self.herb.name_cn, '人参')
        self.assertEqual(self.herb.nature, 'warm')
        self.assertEqual(self.herb.taste, ['sweet', 'bitter'])
        self.assertTrue(self.herb.is_active)
        self.assertFalse(self.herb.is_toxic)

    def test_herb_str(self):
        """Test herb string representation."""
        expected = f"{self.herb.name_cn} ({self.herb.name_en})"
        self.assertEqual(str(self.herb), expected)

    def test_dosage_range_property(self):
        """Test dosage_range property."""
        expected = f"{self.herb.dosage_min}-{self.herb.dosage_max}{self.herb.dosage_unit}"
        self.assertEqual(self.herb.dosage_range, expected)


class ClassicFormulaModelTest(TestCase):
    """Test ClassicFormula model."""

    def setUp(self):
        """Set up test data."""
        self.formula = ClassicFormula.objects.create(
            code='F001',
            name_cn='四君子汤',
            name_en='Four Gentlemen Decoction',
            name_pinyin='Si Jun Zi Tang',
            source='《太平惠民和剂局方》',
            composition='人参、白术、茯苓、甘草',
            functions='益气健脾',
            indications='脾胃气虚证',
            contraindications='阴虚火旺者忌用'
        )

        self.category = HerbCategory.objects.create(
            name_cn='补气药',
            name_en='Qi-Tonifying Herbs'
        )

        self.herb1 = Herb.objects.create(
            code='H001',
            name_cn='人参',
            name_en='Ginseng',
            name_pinyin='Ren Shen',
            category=self.category,
            dosage_min=Decimal('9.00'),
            dosage_max=Decimal('15.00')
        )

        self.herb2 = Herb.objects.create(
            code='H002',
            name_cn='白术',
            name_en='White Atractylodes',
            name_pinyin='Bai Zhu',
            category=self.category,
            dosage_min=Decimal('9.00'),
            dosage_max=Decimal('15.00')
        )

    def test_formula_creation(self):
        """Test classic formula is created successfully."""
        self.assertEqual(self.formula.code, 'F001')
        self.assertEqual(self.formula.name_cn, '四君子汤')
        self.assertTrue(self.formula.is_active)

    def test_formula_str(self):
        """Test formula string representation."""
        expected = f"{self.formula.name_cn} ({self.formula.name_en})"
        self.assertEqual(str(self.formula), expected)

    def test_formula_herbs_relationship(self):
        """Test formula-herb relationship."""
        FormulaHerb.objects.create(
            formula=self.formula,
            herb=self.herb1,
            role='monarch',
            dosage=Decimal('9.00')
        )
        FormulaHerb.objects.create(
            formula=self.formula,
            herb=self.herb2,
            role='minister',
            dosage=Decimal('9.00')
        )

        self.assertEqual(self.formula.formula_herbs.count(), 2)


class PrescriptionModelTest(TestCase):
    """Test Prescription model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testpractitioner',
            email='practitioner@test.com',
            password='testpass123',
            role='practitioner'
        )

        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            chinese_name='测试患者',
            ic_number='123456-78-9012',
            phone='0123456789',
            gender='male',
            date_of_birth='1990-01-01'
        )

        self.category = HerbCategory.objects.create(
            name_cn='补气药',
            name_en='Qi-Tonifying Herbs'
        )

        self.herb1 = Herb.objects.create(
            code='H001',
            name_cn='人参',
            name_en='Ginseng',
            name_pinyin='Ren Shen',
            category=self.category,
            dosage_min=Decimal('3.00'),
            dosage_max=Decimal('9.00'),
            price_per_gram=Decimal('2.50')
        )

        self.herb2 = Herb.objects.create(
            code='H002',
            name_cn='黄芪',
            name_en='Astragalus',
            name_pinyin='Huang Qi',
            category=self.category,
            dosage_min=Decimal('9.00'),
            dosage_max=Decimal('30.00'),
            price_per_gram=Decimal('0.35')
        )

        self.prescription = Prescription.objects.create(
            patient=self.patient,
            practitioner=self.user,
            diagnosis='气虚证',
            treatment_principle='补气健脾',
            doses=7
        )

    def test_prescription_creation(self):
        """Test prescription is created successfully."""
        self.assertEqual(self.prescription.patient, self.patient)
        self.assertEqual(self.prescription.practitioner, self.user)
        self.assertEqual(self.prescription.status, 'draft')
        self.assertIsNotNone(self.prescription.prescription_number)
        self.assertTrue(self.prescription.prescription_number.startswith('RX'))

    def test_prescription_str(self):
        """Test prescription string representation."""
        expected = f"{self.prescription.prescription_number} - {self.patient.full_name}"
        self.assertEqual(str(self.prescription), expected)

    def test_prescription_number_auto_generation(self):
        """Test prescription number is auto-generated."""
        prescription2 = Prescription.objects.create(
            patient=self.patient,
            practitioner=self.user,
            diagnosis='血虚证'
        )
        self.assertIsNotNone(prescription2.prescription_number)
        self.assertNotEqual(
            self.prescription.prescription_number,
            prescription2.prescription_number
        )

    def test_calculate_total(self):
        """Test total price calculation."""
        PrescriptionItem.objects.create(
            prescription=self.prescription,
            herb=self.herb1,
            dosage=Decimal('6.00')
        )
        PrescriptionItem.objects.create(
            prescription=self.prescription,
            herb=self.herb2,
            dosage=Decimal('15.00')
        )

        total = self.prescription.calculate_total()

        # herb1: 2.50 * 6.00 * 7 = 105.00
        # herb2: 0.35 * 15.00 * 7 = 36.75
        # total: 141.75
        expected_total = Decimal('141.75')
        self.assertEqual(total, expected_total)
        self.assertEqual(self.prescription.total_price, expected_total)


class PrescriptionItemModelTest(TestCase):
    """Test PrescriptionItem model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testpractitioner',
            email='practitioner@test.com',
            password='testpass123',
            role='practitioner'
        )

        self.patient = Patient.objects.create(
            first_name='Test',
            last_name='Patient',
            chinese_name='测试患者',
            ic_number='123456-78-9012',
            phone='0123456789',
            gender='male',
            date_of_birth='1990-01-01'
        )

        self.herb = Herb.objects.create(
            code='H001',
            name_cn='甘草',
            name_en='Licorice Root',
            name_pinyin='Gan Cao',
            dosage_min=Decimal('2.00'),
            dosage_max=Decimal('10.00'),
            price_per_gram=Decimal('0.12')
        )

        self.prescription = Prescription.objects.create(
            patient=self.patient,
            practitioner=self.user,
            diagnosis='气虚证',
            doses=7
        )

        self.item = PrescriptionItem.objects.create(
            prescription=self.prescription,
            herb=self.herb,
            dosage=Decimal('6.00'),
            preparation='先煎',
            sequence=1
        )

    def test_prescription_item_creation(self):
        """Test prescription item is created successfully."""
        self.assertEqual(self.item.prescription, self.prescription)
        self.assertEqual(self.item.herb, self.herb)
        self.assertEqual(self.item.dosage, Decimal('6.00'))
        self.assertEqual(self.item.preparation, '先煎')

    def test_prescription_item_str(self):
        """Test prescription item string representation."""
        expected = f"{self.herb.name_cn} {self.item.dosage}g"
        self.assertEqual(str(self.item), expected)

    def test_subtotal_property(self):
        """Test subtotal calculation."""
        # 0.12 * 6.00 * 7 = 5.04
        expected_subtotal = Decimal('5.04')
        self.assertEqual(self.item.subtotal, expected_subtotal)

    def test_subtotal_without_price(self):
        """Test subtotal when herb has no price."""
        herb_no_price = Herb.objects.create(
            code='H999',
            name_cn='测试药',
            name_en='Test Herb',
            name_pinyin='Ce Shi Yao',
            dosage_min=Decimal('3.00'),
            dosage_max=Decimal('10.00')
        )

        item_no_price = PrescriptionItem.objects.create(
            prescription=self.prescription,
            herb=herb_no_price,
            dosage=Decimal('5.00')
        )

        self.assertEqual(item_no_price.subtotal, Decimal('0.00'))


class HerbQueryTest(TestCase):
    """Test herb querying and filtering."""

    def setUp(self):
        """Set up test data."""
        self.category1 = HerbCategory.objects.create(
            name_cn='补气药',
            name_en='Qi-Tonifying Herbs'
        )

        self.category2 = HerbCategory.objects.create(
            name_cn='清热解毒药',
            name_en='Heat-Clearing Herbs'
        )

        Herb.objects.create(
            code='H001',
            name_cn='人参',
            name_en='Ginseng',
            name_pinyin='Ren Shen',
            category=self.category1,
            nature='warm',
            is_active=True
        )

        Herb.objects.create(
            code='H002',
            name_cn='黄连',
            name_en='Coptis',
            name_pinyin='Huang Lian',
            category=self.category2,
            nature='cold',
            is_active=True,
            is_toxic=False
        )

        Herb.objects.create(
            code='H003',
            name_cn='半夏',
            name_en='Pinellia',
            name_pinyin='Ban Xia',
            category=self.category2,
            nature='warm',
            is_active=True,
            is_toxic=True,
            requires_processing=True
        )

    def test_filter_by_category(self):
        """Test filtering herbs by category."""
        qi_herbs = Herb.objects.filter(category=self.category1)
        self.assertEqual(qi_herbs.count(), 1)
        self.assertEqual(qi_herbs.first().name_cn, '人参')

    def test_filter_by_nature(self):
        """Test filtering herbs by nature."""
        warm_herbs = Herb.objects.filter(nature='warm')
        self.assertEqual(warm_herbs.count(), 2)

    def test_filter_toxic_herbs(self):
        """Test filtering toxic herbs."""
        toxic_herbs = Herb.objects.filter(is_toxic=True)
        self.assertEqual(toxic_herbs.count(), 1)
        self.assertEqual(toxic_herbs.first().name_cn, '半夏')

    def test_filter_active_herbs(self):
        """Test filtering active herbs."""
        active_herbs = Herb.objects.filter(is_active=True)
        self.assertEqual(active_herbs.count(), 3)
