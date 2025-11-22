#!/usr/bin/env python
"""
添加示例穴位数据 | Add Sample Acupoint Data
这个脚本添加常用穴位的详细信息到数据库
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhongyi_project.settings')
django.setup()

from acupuncture.models import AcupointReference

# 示例穴位数据 | Sample acupoint data
SAMPLE_ACUPOINTS = [
    {
        'code': 'LI4',
        'chinese_name': '合谷',
        'pinyin_name': 'Hegu',
        'english_name': 'Union Valley',
        'meridian': 'LI',
        'location_chinese': '在手背，第1、2掌骨间，当第2掌骨桡侧的中点处。',
        'location_english': 'On the dorsum of the hand, between the 1st and 2nd metacarpal bones, approximately at the midpoint of the 2nd metacarpal bone on the radial side.',
        'indications': '头痛，目赤肿痛，鼻衄，齿痛，牙关紧闭，口眼歪斜，耳聋，痄腮，咽喉肿痛，热病无汗，多汗，腹痛，便秘，经闭，滞产。',
        'functions': '疏风解表，清热止痛，通经活络，镇静安神。',
        'techniques': '直刺0.5-1寸。孕妇慎用。',
        'precautions': '孕妇禁针。不宜深刺，以免损伤血管。'
    },
    {
        'code': 'ST36',
        'chinese_name': '足三里',
        'pinyin_name': 'Zusanli',
        'english_name': 'Leg Three Miles',
        'meridian': 'ST',
        'location_chinese': '在小腿前外侧，当犊鼻下3寸，距胫骨前缘一横指（中指）。',
        'location_english': 'On the anterior lateral side of the leg, 3 cun below ST35, one finger width lateral to the anterior crest of the tibia.',
        'indications': '胃痛，呕吐，噎膈，腹胀，腹泻，痢疾，便秘，乳痈，肠痈，下肢痿痹，水肿，癫狂，脚气，虚劳羸瘦。',
        'functions': '调理脾胃，补中益气，通经活络，扶正培元。',
        'techniques': '直刺1-2寸。可灸。',
        'precautions': '无特殊禁忌。适合长期保健灸。'
    },
    {
        'code': 'LR3',
        'chinese_name': '太冲',
        'pinyin_name': 'Taichong',
        'english_name': 'Great Surge',
        'meridian': 'LR',
        'location_chinese': '在足背侧，当第1跖骨间隙的后方凹陷处。',
        'location_english': 'On the dorsum of the foot, in the depression distal to the junction of the 1st and 2nd metatarsal bones.',
        'indications': '头痛，眩晕，疝气，月经不调，癃闭，遗尿，小儿惊风，癫狂痫，胁痛，腹胀，黄疸，呕逆，咽痛嗌干，目赤肿痛，膝股内侧痛，足跗肿痛，下肢痿痹。',
        'functions': '平肝熄风，清肝明目，疏肝理气，调经止痛。',
        'techniques': '直刺0.5-1寸。可灸。',
        'precautions': '孕妇慎用。'
    },
    {
        'code': 'PC6',
        'chinese_name': '内关',
        'pinyin_name': 'Neiguan',
        'english_name': 'Inner Pass',
        'meridian': 'PC',
        'location_chinese': '在前臂掌侧，当曲泽与大陵的连线上，腕横纹上2寸，掌长肌腱与桡侧腕屈肌腱之间。',
        'location_english': 'On the palmar side of the forearm, 2 cun above the wrist crease, between the tendons of palmaris longus and flexor carpi radialis.',
        'indications': '心痛，心悸，胸闷，胃痛，呕吐，呃逆，失眠，癫狂痫，中风，偏瘫，哮喘，郁证，眩晕，偏正头痛，热病，产后血晕，肘臂挛痛。',
        'functions': '宁心安神，理气止痛，和胃降逆，宽胸解郁。',
        'techniques': '直刺0.5-1寸。可灸。',
        'precautions': '无特殊禁忌。'
    },
    {
        'code': 'SP6',
        'chinese_name': '三阴交',
        'pinyin_name': 'Sanyinjiao',
        'english_name': 'Three Yin Intersection',
        'meridian': 'SP',
        'location_chinese': '在小腿内侧，当足内踝尖上3寸，胫骨内侧缘后方。',
        'location_english': 'On the tibial aspect of the leg, 3 cun superior to the prominence of the medial malleolus, on the posterior border of the tibia.',
        'indications': '肠鸣腹胀，泄泻，月经不调，崩漏，带下，阴挺，不孕，滞产，遗精，阳痿，遗尿，疝气，失眠，下肢痿痹，脚气，水肿。',
        'functions': '健脾利湿，调补肝肾，养血调经，通经活络。',
        'techniques': '直刺1-1.5寸。可灸。',
        'precautions': '孕妇禁针。'
    },
    {
        'code': 'GB20',
        'chinese_name': '风池',
        'pinyin_name': 'Fengchi',
        'english_name': 'Wind Pool',
        'meridian': 'GB',
        'location_chinese': '在项部，当枕骨之下，与风府相平，胸锁乳突肌与斜方肌上端之间的凹陷处。',
        'location_english': 'In the posterior region of the neck, below the occipital bone, in the depression between the upper portions of sternocleidomastoid and trapezius muscles.',
        'indications': '头痛，眩晕，目赤肿痛，目泪出，鼻渊，鼻衄，耳鸣，耳聋，口眼歪斜，颈项强痛，落枕，感冒，热病，中风，癫痫。',
        'functions': '祛风解表，清头明目，通经活络。',
        'techniques': '针尖微下，向鼻尖方向刺入0.5-1.2寸。可灸。',
        'precautions': '不宜深刺，以免刺伤延髓。'
    },
    {
        'code': 'GV20',
        'chinese_name': '百会',
        'pinyin_name': 'Baihui',
        'english_name': 'Hundred Convergences',
        'meridian': 'GV',
        'location_chinese': '在头部，当前发际正中直上5寸，或两耳尖连线的中点处。',
        'location_english': 'On the head, 5 cun directly above the anterior hairline, or at the midpoint of the line connecting the apices of the two auricles.',
        'indications': '头痛，眩晕，中风，失语，癫狂痫，健忘，失眠，耳鸣，鼻塞，脱肛，阴挺，久泻，久痢，遗尿，小儿惊风。',
        'functions': '醒脑开窍，平肝熄风，升阳固脱，益气健脑。',
        'techniques': '平刺0.5-1寸。可灸。',
        'precautions': '婴幼儿囟门未闭者禁针。'
    },
    {
        'code': 'HT7',
        'chinese_name': '神门',
        'pinyin_name': 'Shenmen',
        'english_name': 'Spirit Gate',
        'meridian': 'HT',
        'location_chinese': '在腕部，腕掌侧横纹尺侧端，尺侧腕屈肌腱的桡侧凹陷处。',
        'location_english': 'On the wrist, at the ulnar end of the transverse crease of the wrist, in the depression on the radial side of the tendon of flexor carpi ulnaris.',
        'indications': '心痛，心烦，惊悸，怔忡，失眠，健忘，痴呆，癫狂痫，晕车。',
        'functions': '养心安神，清心除烦，通经活络。',
        'techniques': '直刺0.3-0.5寸。可灸。',
        'precautions': '无特殊禁忌。'
    },
    {
        'code': 'BL23',
        'chinese_name': '肾俞',
        'pinyin_name': 'Shenshu',
        'english_name': 'Kidney Shu',
        'meridian': 'BL',
        'location_chinese': '在腰部，当第2腰椎棘突下，旁开1.5寸。',
        'location_english': 'In the lumbar region, at the same level as the inferior border of the spinous process of the 2nd lumbar vertebra, 1.5 cun lateral to the posterior midline.',
        'indications': '遗尿，遗精，阳痿，月经不调，白带，水肿，耳鸣，耳聋，腰痛，目眩。',
        'functions': '益肾助阳，强腰健脊，聪耳明目。',
        'techniques': '直刺0.5-1寸。可灸。',
        'precautions': '不宜深刺。'
    },
    {
        'code': 'CV4',
        'chinese_name': '关元',
        'pinyin_name': 'Guanyuan',
        'english_name': 'Gate of Original Qi',
        'meridian': 'CV',
        'location_chinese': '在下腹部，前正中线上，当脐中下3寸。',
        'location_english': 'On the lower abdomen, on the anterior midline, 3 cun below the umbilicus.',
        'indications': '中风脱证，虚劳冷惫，羸瘦无力，少腹疼痛，霍乱吐泻，痢疾，脱肛，疝气，便血，溺血，小便不利，尿频，尿闭，遗尿，遗精，阳痿，早泄，月经不调，经闭，经痛，崩漏，恶露不尽，胞衣不下，阴挺，带下，不孕，中风，尸厥，惊痫，脏躁，水肿。',
        'functions': '培肾固本，补气回阳，调经止带，温下焦。',
        'techniques': '直刺0.5-1寸。可灸。',
        'precautions': '孕妇慎用。'
    },
]

def add_acupoints():
    """添加穴位数据到数据库"""
    print("开始添加穴位数据... | Adding acupoint data...")
    print("=" * 60)

    added = 0
    updated = 0
    errors = 0

    for data in SAMPLE_ACUPOINTS:
        try:
            acupoint, created = AcupointReference.objects.update_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                print(f"✓ 添加 | Added: {acupoint.code} - {acupoint.chinese_name}")
                added += 1
            else:
                print(f"↻ 更新 | Updated: {acupoint.code} - {acupoint.chinese_name}")
                updated += 1
        except Exception as e:
            print(f"✗ 错误 | Error: {data['code']} - {str(e)}")
            errors += 1

    print("=" * 60)
    print(f"\n总结 | Summary:")
    print(f"  新增穴位 | Added: {added}")
    print(f"  更新穴位 | Updated: {updated}")
    print(f"  错误 | Errors: {errors}")
    print(f"  总计 | Total: {added + updated + errors}")
    print("\n✅ 穴位数据添加完成！| Acupoint data added successfully!")

if __name__ == '__main__':
    add_acupoints()
