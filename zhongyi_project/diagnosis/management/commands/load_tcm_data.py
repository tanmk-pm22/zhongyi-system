"""Management command to load initial TCM symptoms and syndromes data."""
from django.core.management.base import BaseCommand
from diagnosis.models import Symptom, Syndrome, SyndromeSysmptomWeight


class Command(BaseCommand):
    help = 'Load initial TCM symptoms and syndromes data'

    def handle(self, *args, **options):
        self.stdout.write('Loading TCM data...')

        # Load symptoms
        symptoms_data = [
            # General
            ('SYM001', 'Fatigue', '疲劳乏力', 'general'),
            ('SYM002', 'Spontaneous sweating', '自汗', 'general'),
            ('SYM003', 'Night sweating', '盗汗', 'general'),
            ('SYM004', 'Aversion to cold', '畏寒', 'general'),
            ('SYM005', 'Aversion to heat', '畏热', 'general'),
            ('SYM006', 'Fever', '发热', 'general'),
            ('SYM007', 'Low-grade fever', '低热', 'general'),

            # Head & Face
            ('SYM010', 'Headache', '头痛', 'head'),
            ('SYM011', 'Dizziness', '头晕', 'head'),
            ('SYM012', 'Tinnitus', '耳鸣', 'head'),
            ('SYM013', 'Blurred vision', '视物模糊', 'head'),
            ('SYM014', 'Dry eyes', '眼干', 'head'),
            ('SYM015', 'Pale face', '面色苍白', 'head'),
            ('SYM016', 'Red face', '面红', 'head'),

            # Chest & Abdomen
            ('SYM020', 'Chest oppression', '胸闷', 'chest'),
            ('SYM021', 'Palpitations', '心悸', 'chest'),
            ('SYM022', 'Shortness of breath', '气短', 'chest'),
            ('SYM023', 'Cough', '咳嗽', 'chest'),
            ('SYM024', 'Abdominal distension', '腹胀', 'chest'),
            ('SYM025', 'Abdominal pain', '腹痛', 'chest'),
            ('SYM026', 'Nausea', '恶心', 'chest'),

            # Limbs
            ('SYM030', 'Cold limbs', '四肢冷', 'limbs'),
            ('SYM031', 'Numb limbs', '四肢麻木', 'limbs'),
            ('SYM032', 'Weak limbs', '四肢无力', 'limbs'),
            ('SYM033', 'Joint pain', '关节痛', 'limbs'),
            ('SYM034', 'Lower back pain', '腰痛', 'limbs'),
            ('SYM035', 'Knee weakness', '膝软', 'limbs'),

            # Sleep
            ('SYM040', 'Insomnia', '失眠', 'sleep'),
            ('SYM041', 'Dream-disturbed sleep', '多梦', 'sleep'),
            ('SYM042', 'Difficulty falling asleep', '难以入睡', 'sleep'),
            ('SYM043', 'Excessive sleep', '嗜睡', 'sleep'),

            # Appetite & Digestion
            ('SYM050', 'Poor appetite', '食欲不振', 'appetite'),
            ('SYM051', 'Loose stools', '便溏', 'appetite'),
            ('SYM052', 'Constipation', '便秘', 'appetite'),
            ('SYM053', 'Dry mouth', '口干', 'appetite'),
            ('SYM054', 'Bitter taste', '口苦', 'appetite'),
            ('SYM055', 'Thirst with desire for cold drinks', '渴喜冷饮', 'appetite'),
            ('SYM056', 'No thirst', '口不渴', 'appetite'),

            # Urination
            ('SYM060', 'Frequent urination', '尿频', 'urination'),
            ('SYM061', 'Scanty dark urine', '尿少色黄', 'urination'),
            ('SYM062', 'Clear profuse urine', '小便清长', 'urination'),
            ('SYM063', 'Nocturia', '夜尿多', 'urination'),

            # Emotion
            ('SYM070', 'Irritability', '烦躁', 'emotion'),
            ('SYM071', 'Depression', '抑郁', 'emotion'),
            ('SYM072', 'Anxiety', '焦虑', 'emotion'),
            ('SYM073', 'Mental restlessness', '心烦', 'emotion'),
        ]

        created_symptoms = 0
        for code, name_en, name_cn, category in symptoms_data:
            symptom, created = Symptom.objects.get_or_create(
                code=code,
                defaults={
                    'name_en': name_en,
                    'name_cn': name_cn,
                    'category': category,
                }
            )
            if created:
                created_symptoms += 1

        self.stdout.write(f'Created {created_symptoms} symptoms')

        # Load syndromes
        syndromes_data = [
            {
                'code': 'SYN001',
                'name_en': 'Qi Deficiency',
                'name_cn': '气虚证',
                'category': 'qi',
                'description': 'A pattern of deficiency characterized by insufficient qi.',
                'etiology': 'Caused by constitutional weakness, chronic illness, overwork, or poor diet.',
                'clinical_manifestations': 'Fatigue, shortness of breath, weak voice, spontaneous sweating.',
                'tongue_signs': 'Pale tongue with thin white coating',
                'pulse_signs': 'Weak, deficient pulse',
                'treatment_principle': 'Tonify qi (补气)',
                'symptoms': [
                    ('SYM001', 2.0, True),   # Fatigue - primary
                    ('SYM002', 1.5, True),   # Spontaneous sweating - primary
                    ('SYM022', 1.5, True),   # Shortness of breath - primary
                    ('SYM032', 1.0, False),  # Weak limbs
                    ('SYM050', 1.0, False),  # Poor appetite
                    ('SYM011', 0.8, False),  # Dizziness
                ]
            },
            {
                'code': 'SYN002',
                'name_en': 'Blood Deficiency',
                'name_cn': '血虚证',
                'category': 'blood',
                'description': 'A pattern characterized by insufficient blood.',
                'etiology': 'Caused by blood loss, poor spleen function, or chronic illness.',
                'clinical_manifestations': 'Pale complexion, dizziness, palpitations, insomnia.',
                'tongue_signs': 'Pale tongue',
                'pulse_signs': 'Thready, weak pulse',
                'treatment_principle': 'Nourish blood (养血)',
                'symptoms': [
                    ('SYM015', 2.0, True),   # Pale face - primary
                    ('SYM011', 1.5, True),   # Dizziness - primary
                    ('SYM021', 1.5, True),   # Palpitations - primary
                    ('SYM040', 1.2, False),  # Insomnia
                    ('SYM031', 1.0, False),  # Numb limbs
                    ('SYM013', 0.8, False),  # Blurred vision
                ]
            },
            {
                'code': 'SYN003',
                'name_en': 'Yin Deficiency',
                'name_cn': '阴虚证',
                'category': 'yin_yang',
                'description': 'A pattern of deficiency heat due to insufficient yin.',
                'etiology': 'Caused by chronic illness, excessive heat, or aging.',
                'clinical_manifestations': 'Night sweating, dry mouth, low-grade fever.',
                'tongue_signs': 'Red tongue with little or no coating',
                'pulse_signs': 'Thready, rapid pulse',
                'treatment_principle': 'Nourish yin, clear deficiency heat (滋阴清热)',
                'symptoms': [
                    ('SYM003', 2.0, True),   # Night sweating - primary
                    ('SYM053', 1.5, True),   # Dry mouth - primary
                    ('SYM007', 1.5, True),   # Low-grade fever - primary
                    ('SYM073', 1.2, False),  # Mental restlessness
                    ('SYM040', 1.0, False),  # Insomnia
                    ('SYM014', 0.8, False),  # Dry eyes
                ]
            },
            {
                'code': 'SYN004',
                'name_en': 'Yang Deficiency',
                'name_cn': '阳虚证',
                'category': 'yin_yang',
                'description': 'A pattern of cold due to insufficient yang.',
                'etiology': 'Caused by constitutional weakness, aging, or chronic cold damage.',
                'clinical_manifestations': 'Aversion to cold, cold limbs, clear urine, loose stools.',
                'tongue_signs': 'Pale, swollen tongue with white moist coating',
                'pulse_signs': 'Deep, slow, weak pulse',
                'treatment_principle': 'Warm and tonify yang (温补阳气)',
                'symptoms': [
                    ('SYM004', 2.0, True),   # Aversion to cold - primary
                    ('SYM030', 2.0, True),   # Cold limbs - primary
                    ('SYM062', 1.5, True),   # Clear profuse urine - primary
                    ('SYM051', 1.2, False),  # Loose stools
                    ('SYM001', 1.0, False),  # Fatigue
                    ('SYM034', 0.8, False),  # Lower back pain
                ]
            },
            {
                'code': 'SYN005',
                'name_en': 'Liver Qi Stagnation',
                'name_cn': '肝气郁结证',
                'category': 'organ',
                'description': 'A pattern of qi stagnation affecting the liver.',
                'etiology': 'Caused by emotional stress, frustration, or anger.',
                'clinical_manifestations': 'Hypochondriac pain, chest oppression, irritability.',
                'tongue_signs': 'Normal or slightly purple tongue',
                'pulse_signs': 'Wiry pulse',
                'treatment_principle': 'Soothe liver, regulate qi (疏肝理气)',
                'symptoms': [
                    ('SYM070', 2.0, True),   # Irritability - primary
                    ('SYM020', 1.5, True),   # Chest oppression - primary
                    ('SYM071', 1.5, False),  # Depression
                    ('SYM024', 1.2, False),  # Abdominal distension
                    ('SYM054', 1.0, False),  # Bitter taste
                    ('SYM040', 0.8, False),  # Insomnia
                ]
            },
            {
                'code': 'SYN006',
                'name_en': 'Phlegm-Dampness',
                'name_cn': '痰湿证',
                'category': 'fluid',
                'description': 'A pattern of excess dampness and phlegm.',
                'etiology': 'Caused by spleen deficiency, excessive dampness, or rich diet.',
                'clinical_manifestations': 'Heaviness, chest oppression, nausea, loose stools.',
                'tongue_signs': 'Swollen tongue with thick greasy coating',
                'pulse_signs': 'Slippery pulse',
                'treatment_principle': 'Resolve phlegm, transform dampness (化痰祛湿)',
                'symptoms': [
                    ('SYM024', 2.0, True),   # Abdominal distension - primary
                    ('SYM026', 1.5, True),   # Nausea - primary
                    ('SYM020', 1.5, False),  # Chest oppression
                    ('SYM051', 1.2, False),  # Loose stools
                    ('SYM001', 1.0, False),  # Fatigue
                    ('SYM043', 0.8, False),  # Excessive sleep
                ]
            },
            {
                'code': 'SYN007',
                'name_en': 'Blood Stasis',
                'name_cn': '血瘀证',
                'category': 'blood',
                'description': 'A pattern of blood stagnation.',
                'etiology': 'Caused by trauma, qi stagnation, or cold congealing blood.',
                'clinical_manifestations': 'Fixed stabbing pain, dark complexion, purple tongue.',
                'tongue_signs': 'Purple or dark tongue with petechiae',
                'pulse_signs': 'Choppy or wiry pulse',
                'treatment_principle': 'Activate blood, resolve stasis (活血化瘀)',
                'symptoms': [
                    ('SYM025', 2.0, True),   # Abdominal pain - primary
                    ('SYM010', 1.5, False),  # Headache
                    ('SYM033', 1.5, False),  # Joint pain
                    ('SYM031', 1.0, False),  # Numb limbs
                    ('SYM021', 0.8, False),  # Palpitations
                ]
            },
            {
                'code': 'SYN008',
                'name_en': 'Damp-Heat',
                'name_cn': '湿热证',
                'category': 'fluid',
                'description': 'A pattern of excess dampness with heat.',
                'etiology': 'Caused by external damp-heat or internal heat with dampness.',
                'clinical_manifestations': 'Fever, thirst, dark urine, bitter taste.',
                'tongue_signs': 'Red tongue with yellow greasy coating',
                'pulse_signs': 'Slippery, rapid pulse',
                'treatment_principle': 'Clear heat, resolve dampness (清热利湿)',
                'symptoms': [
                    ('SYM006', 2.0, True),   # Fever - primary
                    ('SYM061', 1.5, True),   # Scanty dark urine - primary
                    ('SYM054', 1.5, True),   # Bitter taste - primary
                    ('SYM055', 1.2, False),  # Thirst with desire for cold
                    ('SYM024', 1.0, False),  # Abdominal distension
                    ('SYM070', 0.8, False),  # Irritability
                ]
            },
        ]

        created_syndromes = 0
        for syn_data in syndromes_data:
            symptoms_list = syn_data.pop('symptoms')
            syndrome, created = Syndrome.objects.get_or_create(
                code=syn_data['code'],
                defaults=syn_data
            )
            if created:
                created_syndromes += 1

                # Add symptom weights
                for sym_code, weight, is_primary in symptoms_list:
                    try:
                        symptom = Symptom.objects.get(code=sym_code)
                        SyndromeSysmptomWeight.objects.create(
                            syndrome=syndrome,
                            symptom=symptom,
                            weight=weight,
                            is_primary=is_primary
                        )
                    except Symptom.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Symptom {sym_code} not found')
                        )

        self.stdout.write(f'Created {created_syndromes} syndromes')
        self.stdout.write(self.style.SUCCESS('TCM data loaded successfully!'))
