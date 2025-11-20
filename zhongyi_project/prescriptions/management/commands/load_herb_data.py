"""Django management command to load herb data from JSON file."""
import json
import os
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from prescriptions.models import HerbCategory, Herb


class Command(BaseCommand):
    """Load TCM herb data from JSON file."""

    help = '加载中药数据 | Load TCM herb data from JSON file'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--file',
            type=str,
            default='demo/data/herbs_extended.json',
            help='Path to the JSON file containing herb data (relative to project root)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing herb data before loading',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        file_path = options['file']

        # Construct full path
        base_dir = settings.BASE_DIR.parent  # zhongyi_project -> zhongyi-system
        full_path = os.path.join(base_dir, file_path)

        if not os.path.exists(full_path):
            raise CommandError(f'文件不存在 | File does not exist: {full_path}')

        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('清除现有数据... | Clearing existing data...')
            Herb.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('已清除 | Cleared'))

        # Load JSON data
        self.stdout.write(f'正在加载数据 | Loading data from: {full_path}')
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                herbs_data = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f'JSON解析错误 | JSON parse error: {e}')

        # Process each herb
        created_count = 0
        updated_count = 0
        error_count = 0

        for herb_data in herbs_data:
            try:
                # Get or create category
                category_name = herb_data.get('category')
                category = None
                if category_name:
                    category, _ = HerbCategory.objects.get_or_create(
                        name_cn=category_name,
                        defaults={
                            'name_en': self._translate_category(category_name),
                            'description': f'{category_name}类中药',
                        }
                    )

                # Prepare herb data
                code = herb_data['code']
                defaults = {
                    'name_cn': herb_data['name_cn'],
                    'name_en': herb_data['name_en'],
                    'name_pinyin': herb_data.get('name_pinyin', ''),
                    'name_latin': herb_data.get('name_latin', ''),
                    'category': category,
                    'nature': herb_data.get('nature', 'neutral'),
                    'taste': herb_data.get('taste', []),
                    'meridians': herb_data.get('meridians', []),
                    'functions': herb_data.get('functions', ''),
                    'indications': herb_data.get('indications', ''),
                    'contraindications': herb_data.get('contraindications', ''),
                    'dosage_min': Decimal(str(herb_data.get('dosage_min', '3.00'))),
                    'dosage_max': Decimal(str(herb_data.get('dosage_max', '15.00'))),
                    'dosage_unit': herb_data.get('dosage_unit', '克'),
                    'preparation_notes': herb_data.get('preparation_notes', ''),
                    'is_active': herb_data.get('is_active', True),
                    'is_toxic': herb_data.get('is_toxic', False),
                    'requires_processing': herb_data.get('requires_processing', False),
                }

                # Add price if available
                if 'price_per_gram' in herb_data and herb_data['price_per_gram']:
                    defaults['price_per_gram'] = Decimal(str(herb_data['price_per_gram']))

                # Update or create
                herb, created = Herb.objects.update_or_create(
                    code=code,
                    defaults=defaults
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'  ✓ 创建 | Created: {herb.name_cn} ({herb.code})')
                else:
                    updated_count += 1
                    self.stdout.write(f'  ↻ 更新 | Updated: {herb.name_cn} ({herb.code})')

            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(
                        f'  ✗ 错误 | Error processing {herb_data.get("code", "unknown")}: {e}'
                    )
                )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('完成 | Load Complete'))
        self.stdout.write(self.style.SUCCESS(f'创建 | Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'更新 | Updated: {updated_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'错误 | Errors: {error_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def _translate_category(self, category_cn):
        """Translate Chinese category name to English."""
        translations = {
            '解表药': 'Exterior-Releasing Herbs',
            '清热解毒药': 'Heat-Clearing and Toxin-Resolving Herbs',
            '补气药': 'Qi-Tonifying Herbs',
            '补血药': 'Blood-Tonifying Herbs',
            '活血化瘀药': 'Blood-Invigorating and Stasis-Dispelling Herbs',
            '利水渗湿药': 'Water-Draining and Dampness-Percolating Herbs',
            '理气药': 'Qi-Regulating Herbs',
            '化痰止咳平喘药': 'Phlegm-Transforming, Cough-Relieving and Panting-Calming Herbs',
        }
        return translations.get(category_cn, category_cn)
