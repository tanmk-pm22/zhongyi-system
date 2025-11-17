# AI增强中医诊疗系统技术规范

## 版本: 1.0
## 日期: 2025年11月17日

---

## 目录

1. [系统概述](#1-系统概述)
2. [AI辅助病案记录系统](#2-ai辅助病案记录系统)
3. [AI辅助开方系统](#3-ai辅助开方系统)
4. [AI辅助针灸推拿系统](#4-ai辅助针灸推拿系统)
5. [传染病监测与中医方案预警系统](#5-传染病监测与中医方案预警系统)
6. [知识库在线更新机制](#6-知识库在线更新机制)
7. [自动更新提醒系统](#7-自动更新提醒系统)
8. [数据库设计](#8-数据库设计)
9. [系统架构](#9-系统架构)
10. [实施计划](#10-实施计划)

---

## 1. 系统概述

### 1.1 系统目标

构建一个符合马来西亚卫生部标准的AI增强中医诊疗系统，具备以下核心能力：

1. **智能病案记录** - AI自动补全望闻问切信息，分析病因病机
2. **智能开方建议** - 基于辨证论治推荐方剂和中药
3. **智能针灸推拿** - 穴位推荐和可视化图片
4. **传染病预警** - 监测新发传染病，提供中医治疗方案
5. **知识库更新** - 方剂、中药、穴位数据在线更新
6. **更新提醒** - 自动提醒医生新的医学进展

### 1.2 核心AI模块架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AI增强中医诊疗系统                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ AI病案助手   │  │ AI开方助手   │  │ AI针推助手   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│  ┌──────┴────────────────┴────────────────┴──────┐         │
│  │              中医知识图谱引擎                    │         │
│  └──────────────────────┬───────────────────────┘         │
│                         │                                   │
│  ┌──────────────────────┴───────────────────────┐         │
│  │              可更新知识库系统                    │         │
│  ├─────────────┬─────────────┬─────────────────┤         │
│  │ 方剂数据库   │ 中药数据库   │ 穴位数据库       │         │
│  └─────────────┴─────────────┴─────────────────┘         │
│                                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │         传染病监测与预警系统                   │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. AI辅助病案记录系统

### 2.1 功能概述

AI病案助手根据医生输入的部分信息，自动补全望闻问切四诊内容，并分析病因病机，提供辨证建议。

### 2.2 四诊智能采集

#### 2.2.1 望诊AI辅助

```typescript
interface WangZhenAI {
  // 舌诊AI分析
  tongueAnalysis: {
    input: {
      tongueImage?: File;           // 舌象图片（可选）
      manualInput?: {
        tongueBody?: string;        // 舌质
        tongueCoating?: string;     // 舌苔
        tongueShape?: string;       // 舌形
      };
    };

    aiOutput: {
      tongueBodyAnalysis: string;   // 舌质分析：淡红/淡白/红/绛/紫
      coatingAnalysis: string;      // 舌苔分析：薄白/白腻/黄/黄腻/灰黑
      moistureLevel: string;        // 润燥：润/燥/滑
      shapeAnalysis: string;        // 舌形：胖大/瘦薄/齿痕/裂纹

      suggestedFindings: string[];  // AI建议的望诊发现
      possibleSyndromes: string[];  // 可能的证型提示
      confidence: number;           // 置信度 0-100
    };
  };

  // 面诊AI分析
  faceAnalysis: {
    input: {
      faceImage?: File;
      complexion?: string;          // 面色
    };

    aiOutput: {
      complexionType: string;       // 面色类型
      lustre: string;               // 光泽
      specificAreas: {              // 五脏面部分区
        forehead: string;           // 额-心
        nose: string;               // 鼻-脾
        leftCheek: string;          // 左颊-肝
        rightCheek: string;         // 右颊-肺
        chin: string;               // 颏-肾
      };
      suggestions: string[];
    };
  };

  // 形态神态
  bodyAnalysis: {
    bodyType: string;               // 体型
    posture: string;                // 姿态
    spirit: string;                 // 神态
    movement: string;               // 动作
  };
}
```

#### 2.2.2 闻诊AI辅助

```typescript
interface WenZhenAI {
  // 语音分析（可选语音输入）
  voiceAnalysis: {
    input: {
      audioClip?: File;             // 患者语音片段
      manualDescription?: string;   // 医生手动描述
    };

    aiOutput: {
      voiceStrength: string;        // 声音强弱
      voiceTone: string;            // 音调高低
      breathSound: string;          // 呼吸音
      coughType?: string;           // 咳嗽类型
      suggestions: string[];
    };
  };

  // 气味描述
  smellAnalysis: {
    bodyOdor: string;               // 体气
    breathOdor: string;             // 口气
    excretaOdor: string;            // 排泄物气味
  };
}
```

#### 2.2.3 问诊AI辅助（十问）

```typescript
interface WenZhenAI {
  // 十问智能问卷
  tenQuestions: {
    // 1. 寒热
    coldHeat: {
      patientResponse: string;
      aiAnalysis: {
        pattern: '恶寒' | '恶风' | '发热' | '寒热往来' | '潮热' | '五心烦热';
        severity: 'mild' | 'moderate' | 'severe';
        timing: string;
        suggestions: string[];
      };
    };

    // 2. 汗
    sweating: {
      patientResponse: string;
      aiAnalysis: {
        type: '无汗' | '自汗' | '盗汗' | '大汗' | '战汗' | '黄汗';
        location: string[];
        timing: string;
        suggestions: string[];
      };
    };

    // 3. 头身
    headBody: {
      patientResponse: string;
      aiAnalysis: {
        headache?: { location: string; nature: string; timing: string };
        dizziness?: { type: string; severity: string };
        bodyPain?: { location: string[]; nature: string };
        suggestions: string[];
      };
    };

    // 4. 胸腹
    chestAbdomen: {
      patientResponse: string;
      aiAnalysis: {
        chestSymptoms: string[];
        abdomenSymptoms: string[];
        suggestions: string[];
      };
    };

    // 5. 饮食口味
    dietTaste: {
      patientResponse: string;
      aiAnalysis: {
        appetite: string;
        thirst: string;
        taste: string;
        suggestions: string[];
      };
    };

    // 6. 睡眠
    sleep: {
      patientResponse: string;
      aiAnalysis: {
        quality: string;
        issues: string[];      // 失眠/多梦/嗜睡等
        suggestions: string[];
      };
    };

    // 7. 二便
    excretion: {
      patientResponse: string;
      aiAnalysis: {
        stool: { frequency: string; quality: string; issues: string[] };
        urine: { frequency: string; color: string; issues: string[] };
        suggestions: string[];
      };
    };

    // 8. 耳目
    earEye: {
      patientResponse: string;
      aiAnalysis: {
        hearing: string;
        vision: string;
        issues: string[];
        suggestions: string[];
      };
    };

    // 9. 经带（女性）
    menstruation: {
      patientResponse: string;
      aiAnalysis: {
        cycle: string;
        volume: string;
        color: string;
        painLevel: string;
        leukorrhea: string;
        suggestions: string[];
      };
    };

    // 10. 旧病史
    medicalHistory: {
      patientResponse: string;
      aiAnalysis: {
        chronicConditions: string[];
        relevantHistory: string[];
        suggestions: string[];
      };
    };
  };

  // AI自动补全功能
  autoComplete: {
    // 根据已输入症状，推荐可能遗漏的问诊项目
    suggestedQuestions: string[];
    // 根据症状群，自动关联相关问诊
    relatedSymptoms: string[];
  };
}
```

#### 2.2.4 切诊AI辅助

```typescript
interface QieZhenAI {
  // 脉诊
  pulseAnalysis: {
    input: {
      // 智能脉诊仪数据（可选）
      pulseWaveform?: {
        leftCun: number[];
        leftGuan: number[];
        leftChi: number[];
        rightCun: number[];
        rightGuan: number[];
        rightChi: number[];
      };
      // 医生手动输入
      manualInput?: {
        pulseRate: number;
        pulseRhythm: string;
        pulseStrength: string;
        pulseDepth: string;
        pulseWidth: string;
        pulseTension: string;
      };
    };

    aiOutput: {
      // 脉象综合判断
      mainPulseType: string;        // 主脉：浮/沉/迟/数/虚/实等28脉
      compoundPulse: string[];      // 兼脉

      // 三部九候分析
      threeRegions: {
        cun: { left: string; right: string };   // 寸-心肺
        guan: { left: string; right: string };  // 关-肝脾
        chi: { left: string; right: string };   // 尺-肾
      };

      // AI分析
      organImplication: string[];   // 脏腑提示
      pathologyHint: string[];      // 病理提示
      suggestions: string[];
      confidence: number;
    };
  };

  // 按诊
  palpation: {
    skinTemperature: string;
    skinMoisture: string;
    abdominalPalpation: {
      tenderness: string[];
      masses: string[];
      tension: string;
    };
    acupointTenderness: string[];   // 穴位压痛
  };
}
```

### 2.3 病因病机AI分析

```typescript
interface PathogenesisAI {
  // 综合四诊信息
  input: {
    wangZhen: WangZhenAI;
    wenZhen: WenZhenAI;
    wenZhenQuestions: WenZhenAI;
    qieZhen: QieZhenAI;

    // 患者基本信息
    patientProfile: {
      age: number;
      gender: string;
      constitution: string;     // 体质类型
      lifestyle: string[];
      environment: string;      // 居住环境
      occupation: string;
    };
  };

  // AI分析输出
  output: {
    // 病因分析
    etiology: {
      externalCauses: {         // 外因
        sixExcesses: string[];  // 六淫：风寒暑湿燥火
        epidemic: string[];     // 疫疠
      };
      internalCauses: {         // 内因
        sevenEmotions: string[]; // 七情：喜怒忧思悲恐惊
      };
      otherCauses: {            // 不内外因
        diet: string[];
        fatigue: string[];
        trauma: string[];
        phlegmStasis: string[];
      };

      primaryCause: string;     // 主要病因
      secondaryCauses: string[]; // 次要病因
      confidence: number;
    };

    // 病机分析
    pathogenesis: {
      // 病位
      diseaseLocation: {
        organs: string[];       // 脏腑：心肝脾肺肾
        meridians: string[];    // 经络
        tissues: string[];      // 组织：气血津液
        regions: string[];      // 部位：表里上下
      };

      // 病性
      diseaseNature: {
        coldHeat: '寒' | '热' | '寒热错杂';
        deficiencyExcess: '虚' | '实' | '虚实夹杂';
        yinYang: string;
      };

      // 病势
      diseaseTrend: {
        stage: '初期' | '中期' | '后期' | '恢复期';
        prognosis: string;
        tendency: '好转' | '稳定' | '恶化';
      };

      // 病机描述
      mechanismDescription: string;  // AI生成的病机分析文字

      confidence: number;
    };

    // 辨证结果
    syndromeAnalysis: {
      // 八纲辨证
      eightPrinciples: {
        exterior_interior: '表证' | '里证' | '半表半里';
        cold_heat: '寒证' | '热证' | '寒热错杂';
        deficiency_excess: '虚证' | '实证' | '虚实夹杂';
        yin_yang: '阴证' | '阳证' | '阴阳两虚';
      };

      // 脏腑辨证
      organSyndrome: string[];

      // 气血津液辨证
      qiBloodFluid: string[];

      // 经络辨证
      meridianSyndrome: string[];

      // 六经辨证（外感病）
      sixMeridians?: string;

      // 卫气营血辨证（温病）
      weiQiYingXue?: string;

      // 三焦辨证
      tripleWarmer?: string;

      // 最终证型
      finalSyndrome: {
        primary: string;        // 主证
        secondary: string[];    // 兼证
        tcmDiagnosis: string;   // 中医诊断
      };

      confidence: number;
    };

    // 治则治法建议
    treatmentPrinciple: {
      mainPrinciple: string;    // 主要治则
      methods: string[];        // 治法
      cautions: string[];       // 注意事项
    };
  };

  // AI解释和依据
  explanation: {
    reasoning: string;          // AI推理过程说明
    classicReferences: string[]; // 引用经典条文
    modernEvidence: string[];   // 现代研究支持
  };
}
```

### 2.4 AI自动补全界面设计

```
┌─────────────────────────────────────────────────────────────┐
│  病案记录 - AI辅助模式                               [保存] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  患者: 张三  性别: 男  年龄: 45岁                            │
│                                                             │
│  ┌─ 望诊 ─────────────────────────────────────────────┐    │
│  │ 舌象: [淡红舌，薄白苔    ] [📷上传舌象] [🤖AI分析]    │    │
│  │                                                     │    │
│  │ 💡 AI建议补充：                                      │    │
│  │ • 舌形：正常/胖大/瘦薄？                              │    │
│  │ • 舌下络脉：正常/迂曲/青紫？                          │    │
│  │ [采纳建议]                                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ 问诊 ─────────────────────────────────────────────┐    │
│  │ 主诉: [头痛3天，伴恶寒发热                        ]   │    │
│  │                                                     │    │
│  │ 🤖 AI智能问诊引导：                                  │    │
│  │ 基于主诉，建议询问以下问题：                          │    │
│  │ ✅ 发热程度和时间特点？                              │    │
│  │ ✅ 头痛部位和性质？                                  │    │
│  │ ⬜ 有无汗出？                                       │    │
│  │ ⬜ 口渴否？饮水情况？                                │    │
│  │ ⬜ 二便情况？                                       │    │
│  │ [自动生成问诊记录]                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ 切诊 ─────────────────────────────────────────────┐    │
│  │ 脉象: [浮紧                                      ]   │    │
│  │                                                     │    │
│  │ 💡 AI补充分析：                                      │    │
│  │ 浮脉主表证，紧脉主寒、主痛                            │    │
│  │ 结合症状，提示外感风寒表实证                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─ 病因病机分析 ──────────────────────── [🤖AI分析] ─┐    │
│  │                                                     │    │
│  │ 病因：风寒外袭                                       │    │
│  │ 病位：太阳经，肺卫                                   │    │
│  │ 病性：表实寒证                                       │    │
│  │ 病机：风寒束表，卫阳被遏，营阴郁滞                     │    │
│  │                                                     │    │
│  │ 证型：风寒表实证                                     │    │
│  │ 治则：辛温解表，宣肺散寒                              │    │
│  │                                                     │    │
│  │ 📚 经典依据：                                        │    │
│  │ 《伤寒论》："太阳病，头痛发热，身疼腰痛，骨节疼痛，     │    │
│  │  恶风无汗而喘者，麻黄汤主之。"                        │    │
│  │                                                     │    │
│  │ 置信度: 92%  [采纳] [修改] [重新分析]                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. AI辅助开方系统

### 3.1 功能概述

基于辨证结果，AI推荐最适合的方剂和中药，并结合现代研究提供最新的用药建议。

### 3.2 方剂推荐引擎

```typescript
interface FormulaRecommendationAI {
  // 输入
  input: {
    syndrome: string;           // 证型
    symptoms: string[];         // 症状列表
    patientProfile: {
      age: number;
      gender: string;
      weight: number;
      allergies: string[];
      chronicConditions: string[];
      currentMedications: string[];  // 包括西药
      pregnancy?: boolean;
      breastfeeding?: boolean;
    };
    treatmentGoal: string;      // 治疗目标
  };

  // AI推荐输出
  output: {
    // 主方推荐
    primaryFormula: {
      formulaId: string;
      name: string;             // 方剂名
      pinyin: string;
      source: string;           // 出处：《伤寒论》等
      category: string;         // 方剂分类

      // 原方组成
      originalComposition: {
        herb: string;
        dosage: string;
        role: '君' | '臣' | '佐' | '使';
      }[];

      // AI调整建议
      adjustedComposition: {
        herb: string;
        originalDosage: string;
        adjustedDosage: string;
        adjustmentReason: string;
      }[];

      // 功效
      functions: string[];
      indications: string[];

      // 现代研究
      modernResearch: {
        pharmacology: string[];     // 现代药理
        clinicalStudies: string[];  // 临床研究
        evidenceLevel: string;      // 证据等级
      };

      // 匹配度
      matchScore: number;           // 0-100
      matchReason: string;
    };

    // 备选方推荐
    alternativeFormulas: {
      formulaId: string;
      name: string;
      matchScore: number;
      differenceFromPrimary: string;
    }[];

    // 加减建议
    modifications: {
      condition: string;        // 兼证/症状
      addHerbs: { herb: string; dosage: string; reason: string }[];
      removeHerbs: { herb: string; reason: string }[];
    }[];

    // 安全检查
    safetyCheck: {
      contraindications: string[];
      drugInteractions: {
        herb: string;
        interactsWith: string;
        severity: 'high' | 'medium' | 'low';
        description: string;
      }[];
      pregnancyWarnings: string[];
      allergyWarnings: string[];
      dosageWarnings: string[];
    };
  };
}
```

### 3.3 中药智能推荐

```typescript
interface HerbRecommendationAI {
  // 单味药推荐
  singleHerbRecommendation: {
    input: {
      targetFunction: string;   // 目标功效
      syndrome: string;
    };

    output: {
      recommendedHerbs: {
        herbId: string;
        chineseName: string;
        pinyin: string;
        latinName: string;

        // 基本信息
        properties: {
          nature: string;       // 四气：寒热温凉
          flavor: string[];     // 五味：酸苦甘辛咸
          meridians: string[];  // 归经
        };

        // 功效
        functions: string[];
        indications: string[];

        // 用量
        dosage: {
          standard: string;
          decoction: string;
          powder: string;
          maxDaily: string;
        };

        // 现代研究
        modernResearch: {
          activeCompounds: string[];
          pharmacology: string[];
          clinicalApplications: string[];
        };

        // 注意事项
        cautions: string[];
        contraindications: string[];

        matchScore: number;
      }[];
    };
  };

  // 药对推荐
  herbPairRecommendation: {
    forHerb: string;
    synergisticPairs: {
      partnerHerb: string;
      combinedEffect: string;
      classicSource: string;
    }[];
  };
}
```

### 3.4 处方安全检查系统

```typescript
interface PrescriptionSafetyAI {
  // 配伍禁忌检查
  compatibilityCheck: {
    // 十八反
    eighteenIncompatibles: {
      found: boolean;
      details: {
        herb1: string;
        herb2: string;
        type: string;
        warning: string;
      }[];
    };

    // 十九畏
    nineteenClashes: {
      found: boolean;
      details: {
        herb1: string;
        herb2: string;
        effect: string;
        warning: string;
      }[];
    };

    // 妊娠禁忌
    pregnancyContraindications: {
      found: boolean;
      herbs: {
        herb: string;
        category: '禁用' | '慎用';
        reason: string;
      }[];
    };
  };

  // 中西药相互作用
  herbDrugInteraction: {
    interactions: {
      herb: string;
      drug: string;
      mechanism: string;
      clinicalEffect: string;
      severity: 'contraindicated' | 'major' | 'moderate' | 'minor';
      management: string;
      references: string[];
    }[];
  };

  // 剂量检查
  dosageCheck: {
    overdoseWarnings: {
      herb: string;
      prescribed: string;
      maximum: string;
      warning: string;
    }[];

    underdoseWarnings: {
      herb: string;
      prescribed: string;
      minimum: string;
      warning: string;
    }[];
  };

  // 特殊人群检查
  specialPopulationCheck: {
    pediatric: string[];
    geriatric: string[];
    renalImpairment: string[];
    hepaticImpairment: string[];
  };
}
```

### 3.5 开方界面设计

```
┌─────────────────────────────────────────────────────────────┐
│  开方 - AI辅助模式                                   [保存]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  诊断: 风寒表实证                                            │
│  治则: 辛温解表，宣肺散寒                                     │
│                                                             │
│  ┌─ AI方剂推荐 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🥇 推荐方剂: 麻黄汤                                   │   │
│  │     出处: 《伤寒论》                                   │   │
│  │     匹配度: 95%                                       │   │
│  │                                                       │   │
│  │  📋 组成:                                             │   │
│  │  ┌────────┬────────┬────────┬──────────────────┐     │   │
│  │  │ 药物    │ 剂量    │ 角色   │ AI调整建议        │     │   │
│  │  ├────────┼────────┼────────┼──────────────────┤     │   │
│  │  │ 麻黄    │ 9g     │ 君     │ 因患者年龄，减至6g │     │   │
│  │  │ 桂枝    │ 6g     │ 臣     │ -                │     │   │
│  │  │ 杏仁    │ 9g     │ 佐     │ -                │     │   │
│  │  │ 炙甘草  │ 3g     │ 使     │ -                │     │   │
│  │  └────────┴────────┴────────┴──────────────────┘     │   │
│  │                                                       │   │
│  │  📊 现代研究支持:                                      │   │
│  │  • 麻黄碱具有解热、抗病毒作用                           │   │
│  │  • 临床研究显示有效率87.5%（证据等级B）                  │   │
│  │                                                       │   │
│  │  [采用此方] [查看其他推荐]                              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 加减调整 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  💡 AI建议加减:                                       │   │
│  │                                                       │   │
│  │  兼头痛甚 → 加 白芷 10g, 川芎 6g                       │   │
│  │  兼咳嗽痰多 → 加 半夏 9g, 陈皮 6g                      │   │
│  │  兼咽痛 → 减 麻黄, 加 牛蒡子 10g                       │   │
│  │                                                       │   │
│  │  [应用建议]                                           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 安全检查 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ✅ 配伍禁忌检查: 通过                                 │   │
│  │  ✅ 十八反十九畏: 无冲突                               │   │
│  │  ⚠️ 中西药相互作用:                                   │   │
│  │     麻黄 + 患者正在服用的降压药                         │   │
│  │     → 麻黄可能减弱降压效果，建议监测血压                 │   │
│  │  ✅ 剂量检查: 正常范围                                 │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 最终处方 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  麻黄 6g, 桂枝 6g, 杏仁 9g, 炙甘草 3g                  │   │
│  │  白芷 10g, 川芎 6g                                    │   │
│  │                                                       │   │
│  │  剂数: [3] 剂    煎服法: [水煎服，日一剂，分二次温服]     │   │
│  │                                                       │   │
│  │  [打印处方] [发送至药房]                                │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. AI辅助针灸推拿系统

### 4.1 穴位数据库设计

```typescript
interface AcupointDatabase {
  // 穴位基本信息
  acupoint: {
    acupointId: string;

    // 名称
    names: {
      chinese: string;          // 中文名
      pinyin: string;           // 拼音
      english: string;          // 英文名
      code: string;             // 国际代码 (如 LI4)
      alternativeNames: string[]; // 别名
    };

    // 归经
    meridian: {
      name: string;             // 经络名称
      type: '正经' | '奇经' | '经外奇穴';
      sequence: number;         // 经穴序号
    };

    // 定位
    location: {
      // 文字描述
      description: string;

      // 解剖定位
      anatomy: {
        region: string;         // 解剖区域
        muscles: string[];      // 相关肌肉
        nerves: string[];       // 相关神经
        vessels: string[];      // 相关血管
        depth: string;          // 针刺深度
      };

      // 3D坐标（用于可视化）
      coordinates: {
        x: number;
        y: number;
        z: number;
        bodyPart: string;
      };

      // 简便取穴法
      easyLocation: string;
    };

    // 功效主治
    functions: {
      effects: string[];        // 功效
      indications: string[];    // 主治

      // 按系统分类的主治
      bySystem: {
        respiratory: string[];
        digestive: string[];
        cardiovascular: string[];
        neurological: string[];
        musculoskeletal: string[];
        gynecological: string[];
        urological: string[];
        psychological: string[];
        other: string[];
      };

      // 特定作用
      specialActions: string[]; // 如：急救穴、回阳穴等
    };

    // 操作方法
    techniques: {
      needling: {
        angle: string;          // 进针角度
        depth: string;          // 针刺深度范围
        sensation: string;      // 针感
        manipulation: string[]; // 手法
        cautions: string[];     // 注意事项
      };

      moxibustion: {
        suitable: boolean;
        method: string;
        duration: string;
        cautions: string[];
      };

      cupping: {
        suitable: boolean;
        method: string;
        duration: string;
      };

      acupressure: {
        method: string;
        pressure: string;
        duration: string;
      };
    };

    // 配伍
    combinations: {
      acupoint: string;
      combinedEffect: string;
      indication: string;
      source: string;
    }[];

    // 禁忌
    contraindications: string[];

    // 现代研究
    modernResearch: {
      mechanisms: string[];
      clinicalStudies: string[];
      evidenceLevel: string;
    };

    // 图片资源
    images: {
      locationImage: string;    // 定位图URL
      anatomyImage: string;     // 解剖图URL
      needlingImage: string;    // 针刺图URL
      video?: string;           // 教学视频URL
    };
  };
}
```

### 4.2 穴位图片资源管理

```typescript
interface AcupointImageSystem {
  // 图片类型
  imageTypes: {
    // 经络循行图
    meridianCharts: {
      meridianId: string;
      fullBodyImage: string;      // 全身循行图
      detailImages: string[];     // 局部详图
      acupointsOnPath: string[];  // 经上穴位标注
    };

    // 穴位定位图
    acupointLocationImages: {
      acupointId: string;
      surfaceAnatomyImage: string;  // 体表定位图
      crossSectionImage: string;    // 横截面图
      measurementImage: string;     // 骨度分寸图
      landmarkImage: string;        // 标志物参照图
    };

    // 3D人体模型
    threeDModel: {
      modelType: 'male' | 'female';
      format: 'glb' | 'obj';
      features: {
        rotatable: boolean;
        zoomable: boolean;
        layerToggle: boolean;    // 可切换皮肤/肌肉/骨骼层
        acupointMarkers: boolean;
        meridianLines: boolean;
      };
    };

    // 操作示范图
    techniqueImages: {
      acupointId: string;
      needlingDemo: string[];
      moxibustionDemo: string[];
      massageDemo: string[];
    };
  };

  // 图片标注系统
  imageAnnotation: {
    // 可在图片上标注
    annotations: {
      type: 'point' | 'line' | 'area' | 'text';
      coordinates: any;
      label: string;
      color: string;
    }[];

    // 治疗记录标注
    treatmentMarking: {
      sessionId: string;
      markedPoints: {
        acupointId: string;
        technique: string;
        notes: string;
      }[];
      savedImage: string;       // 保存标注后的图片
    };
  };
}
```

### 4.3 AI穴位推荐系统

```typescript
interface AcupointRecommendationAI {
  input: {
    syndrome: string;           // 证型
    symptoms: string[];         // 症状
    diseaseLocation: string[];  // 病位
    treatmentGoal: string;      // 治疗目标

    patientProfile: {
      age: number;
      gender: string;
      constitution: string;
      contraindications: string[];
    };

    previousTreatments?: {
      acupoints: string[];
      response: string;
    };
  };

  output: {
    // 推荐穴位处方
    acupointPrescription: {
      // 主穴
      primaryPoints: {
        acupointId: string;
        name: string;
        code: string;

        selectionReason: string;  // 选穴依据
        technique: {
          method: string;         // 针刺/灸/推拿
          manipulation: string;   // 手法
          duration: string;       // 时间
          reinforceReduce: '补' | '泻' | '平补平泻';
        };

        expectedEffect: string;
      }[];

      // 配穴
      secondaryPoints: {
        acupointId: string;
        name: string;
        code: string;

        pairingWith: string;      // 与哪个主穴配伍
        combinedEffect: string;   // 配伍效果
        technique: any;
      }[];

      // 随症加减穴
      symptomBasedAdditions: {
        symptom: string;
        addPoints: {
          acupointId: string;
          name: string;
          reason: string;
        }[];
      }[];
    };

    // 经典依据
    classicReferences: {
      source: string;
      content: string;
    }[];

    // 现代研究支持
    modernEvidence: {
      study: string;
      finding: string;
      evidenceLevel: string;
    }[];

    // 治疗方案
    treatmentPlan: {
      frequency: string;        // 频次：每日/隔日/每周
      sessions: number;         // 疗程次数
      duration: string;         // 每次时间
      precautions: string[];    // 注意事项
    };

    // 可视化
    visualization: {
      bodyChartUrl: string;     // 带标注的人体图
      selectedPointsImage: string;
    };

    confidence: number;
  };
}
```

### 4.4 推拿手法数据库

```typescript
interface TuinaTechniqueDatabase {
  technique: {
    techniqueId: string;

    // 名称
    names: {
      chinese: string;
      pinyin: string;
      english: string;
      category: '成人推拿' | '小儿推拿';
    };

    // 分类
    classification: {
      type: '摆动类' | '摩擦类' | '挤压类' | '叩击类' | '振动类' | '运动关节类';
      subtype: string;
    };

    // 操作方法
    operation: {
      description: string;        // 文字描述
      steps: string[];            // 分步骤
      keyPoints: string[];        // 操作要领

      parameters: {
        force: string;            // 力度
        frequency: string;        // 频率
        duration: string;         // 持续时间
        direction: string;        // 方向
      };
    };

    // 适用部位
    applicableAreas: {
      bodyParts: string[];
      acupoints: string[];
      meridians: string[];
    };

    // 功效主治
    functions: {
      effects: string[];
      indications: string[];
      mechanisms: string[];
    };

    // 禁忌症
    contraindications: string[];

    // 媒体资源
    media: {
      images: string[];
      demonstrationVideo: string;
      animationUrl: string;
    };
  };

  // 推拿治疗方案
  treatmentProtocol: {
    condition: string;           // 病症

    // 手法组合
    techniqueSequence: {
      order: number;
      techniqueId: string;
      bodyPart: string;
      duration: string;
      repetitions: number;
      notes: string;
    }[];

    totalDuration: string;
    frequency: string;
    courseOfTreatment: string;
  };
}
```

### 4.5 针灸推拿界面设计

```
┌─────────────────────────────────────────────────────────────┐
│  针灸治疗 - AI辅助模式                               [保存]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  诊断: 肝郁气滞证 - 胁肋疼痛                                  │
│                                                             │
│  ┌─ AI穴位推荐 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📍 主穴推荐:                                         │   │
│  │                                                       │   │
│  │  1. 太冲 (LR3)                                        │   │
│  │     选穴依据: 肝经原穴，疏肝理气要穴                    │   │
│  │     手法: 泻法，捻转提插                               │   │
│  │     [查看定位图] [查看解剖图]                          │   │
│  │                                                       │   │
│  │  2. 期门 (LR14)                                       │   │
│  │     选穴依据: 肝之募穴，治疗胁痛要穴                    │   │
│  │     手法: 平补平泻                                    │   │
│  │     [查看定位图] [查看解剖图]                          │   │
│  │                                                       │   │
│  │  3. 阳陵泉 (GB34)                                     │   │
│  │     选穴依据: 八会穴之筋会，配合疏肝                    │   │
│  │     手法: 泻法                                        │   │
│  │     [查看定位图] [查看解剖图]                          │   │
│  │                                                       │   │
│  │  📍 配穴推荐:                                         │   │
│  │  • 合谷 (LI4) - 配太冲为四关穴，行气活血                │   │
│  │  • 内关 (PC6) - 宽胸理气                              │   │
│  │                                                       │   │
│  │  💡 随症加减:                                         │   │
│  │  • 胁痛甚 → 加支沟 (SJ6)                              │   │
│  │  • 口苦 → 加胆俞 (BL19)                               │   │
│  │  • 失眠 → 加神门 (HT7)                                │   │
│  │                                                       │   │
│  │  [采纳推荐] [手动调整]                                 │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 穴位可视化 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ┌─────────────────┐  ┌─────────────────────────┐    │   │
│  │  │                 │  │                         │    │   │
│  │  │   [3D人体模型]   │  │  选中穴位: 太冲 (LR3)    │    │   │
│  │  │                 │  │                         │    │   │
│  │  │  🔴 太冲        │  │  [足部定位图]            │    │   │
│  │  │  🔴 期门        │  │                         │    │   │
│  │  │  🔴 阳陵泉      │  │  定位: 足背第1、2跖骨    │    │   │
│  │  │  🟡 合谷        │  │  结合部之前凹陷中        │    │   │
│  │  │  🟡 内关        │  │                         │    │   │
│  │  │                 │  │  深度: 0.5-0.8寸        │    │   │
│  │  │  [旋转] [缩放]  │  │  角度: 直刺             │    │   │
│  │  │  [显示经络]     │  │                         │    │   │
│  │  └─────────────────┘  │  [播放取穴视频]          │    │   │
│  │                       └─────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 治疗记录 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  选用穴位:                                            │   │
│  │  ☑ 太冲(双) ☑ 期门(双) ☑ 阳陵泉(双)                  │   │
│  │  ☑ 合谷(双) ☑ 内关(双) ☐ 支沟                        │   │
│  │                                                       │   │
│  │  操作记录:                                            │   │
│  │  留针时间: [30] 分钟                                  │   │
│  │  电针: ☑ 是  穴位: [太冲-阳陵泉]  频率: [2Hz]          │   │
│  │  得气情况: [良好，有酸胀感                          ]   │   │
│  │  不良反应: [无                                     ]   │   │
│  │  患者反馈: [治疗后胁痛减轻                          ]   │   │
│  │                                                       │   │
│  │  [在人体图上标注] [保存记录]                           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 疗程计划 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  建议疗程: 隔日1次，10次为一疗程                        │   │
│  │  下次治疗: [2025-11-19]  [添加到预约]                   │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 传染病监测与中医方案预警系统

### 5.1 系统概述

监测新发传染病和感染病，自动提醒医生并提供最新的中医治疗方案，整合WHO、马来西亚卫生部、中国国家中医药管理局等权威来源。

### 5.2 数据源整合

```typescript
interface EpidemicDataSources {
  // 国际数据源
  international: {
    WHO: {
      endpoint: string;
      dataTypes: ['Disease Outbreak News', 'Weekly Epidemiological Record'];
      updateFrequency: 'daily';
    };

    ProMED: {
      endpoint: string;
      dataTypes: ['Outbreak Reports'];
      updateFrequency: 'real-time';
    };
  };

  // 马来西亚本地数据源
  malaysia: {
    MOH: {
      endpoint: string;
      dataTypes: ['Notifiable Diseases', 'Outbreak Alerts'];
      updateFrequency: 'daily';
    };

    MySejahtera: {
      endpoint: string;
      dataTypes: ['Regional Health Data'];
    };
  };

  // 中国中医药数据源
  tcmSources: {
    NATCM: {
      // 国家中医药管理局
      endpoint: string;
      dataTypes: ['TCM Treatment Protocols', 'Expert Consensus'];
      updateFrequency: 'as-published';
    };

    CACMS: {
      // 中国中医科学院
      endpoint: string;
      dataTypes: ['Research Papers', 'Clinical Guidelines'];
    };
  };
}
```

### 5.3 传染病监测系统

```typescript
interface EpidemicMonitoringSystem {
  // 疾病监测配置
  monitoring: {
    // 监测的疾病类型
    diseases: {
      respiratory: string[];     // 呼吸道传染病
      gastrointestinal: string[];// 消化道传染病
      vectorBorne: string[];     // 虫媒传染病
      zoonotic: string[];        // 人畜共患病
      emerging: string[];        // 新发传染病
    };

    // 监测指标
    indicators: {
      caseCount: number;         // 病例数阈值
      growthRate: number;        // 增长率阈值
      geographicSpread: number;  // 地理扩散
      severity: number;          // 严重程度
      novelty: boolean;          // 新型病原
    };

    // 监测区域
    regions: {
      local: string[];           // 当地区域
      national: string[];        // 全国
      international: string[];   // 国际（重点关注国家）
    };
  };

  // 预警生成
  alertGeneration: {
    // 预警等级
    alertLevels: {
      level1_info: {
        trigger: string;
        color: 'blue';
        action: 'Inform';
      };
      level2_attention: {
        trigger: string;
        color: 'yellow';
        action: 'Monitor closely';
      };
      level3_warning: {
        trigger: string;
        color: 'orange';
        action: 'Prepare response';
      };
      level4_emergency: {
        trigger: string;
        color: 'red';
        action: 'Immediate action';
      };
    };

    // 预警内容
    alertContent: {
      diseaseInfo: {
        name: string;
        pathogen: string;
        transmissionMode: string;
        incubationPeriod: string;
        symptoms: string[];
      };

      epidemiologicalData: {
        affectedRegions: string[];
        caseCount: number;
        fatalityRate: number;
        trend: 'increasing' | 'stable' | 'decreasing';
      };

      clinicalFeatures: {
        commonSymptoms: string[];
        severeSymptoms: string[];
        labFindings: string[];
        differentialDiagnosis: string[];
      };
    };
  };
}
```

### 5.4 中医治疗方案推送

```typescript
interface TCMTreatmentProtocol {
  // 方案基本信息
  protocolInfo: {
    protocolId: string;
    disease: string;
    version: string;
    issueDate: string;
    source: string;             // 来源机构
    authorityLevel: string;     // 权威级别
  };

  // 中医认识
  tcmUnderstanding: {
    diseaseCategory: string;    // 中医归属（如：温病、疫病）
    etiology: string;           // 病因：疫疠之气等
    pathogenesis: string;       // 病机
    diseaseLocation: string[];  // 病位
    transmission: string;       // 传变规律
  };

  // 分期分型治疗
  treatmentByStage: {
    stage: string;              // 分期：初期/中期/重症期/恢复期

    // 中医证型
    syndromes: {
      syndromeName: string;
      clinicalManifestations: {
        symptoms: string[];
        tongue: string;
        pulse: string;
      };

      // 治法方药
      treatment: {
        principle: string;      // 治则
        formula: {
          name: string;
          composition: {
            herb: string;
            dosage: string;
          }[];
          modification: string;
          usage: string;
        };

        // 中成药
        patentMedicine?: {
          name: string;
          dosage: string;
          usage: string;
        }[];
      };

      // 针灸方案
      acupuncture?: {
        points: string[];
        technique: string;
        frequency: string;
      };

      // 其他疗法
      otherTherapies?: string[];
    }[];
  }[];

  // 预防方案
  prevention: {
    // 预防方药
    preventiveFormula: {
      name: string;
      composition: any[];
      usage: string;
      suitableFor: string;
    };

    // 艾灸预防
    moxibustion: {
      points: string[];
      method: string;
      frequency: string;
    };

    // 香囊/熏香
    aromatic: {
      composition: string[];
      usage: string;
    };

    // 饮食建议
    dietaryAdvice: string[];

    // 起居建议
    lifestyleAdvice: string[];
  };

  // 参考文献
  references: string[];
}
```

### 5.5 预警通知系统

```typescript
interface AlertNotificationSystem {
  // 通知渠道
  channels: {
    inApp: {
      popup: boolean;
      dashboard: boolean;
      badge: boolean;
    };

    email: {
      enabled: boolean;
      template: string;
    };

    sms: {
      enabled: boolean;
      forEmergency: boolean;
    };

    pushNotification: {
      enabled: boolean;
    };
  };

  // 通知内容模板
  notificationTemplate: {
    title: string;
    summary: string;

    sections: {
      epidemicSituation: string;
      clinicalAlert: string;
      tcmProtocol: string;
      actionRequired: string;
    };

    attachments: {
      fullProtocol: string;     // PDF链接
      quickReference: string;   // 快速参考卡
    };

    actions: {
      viewDetails: string;
      downloadProtocol: string;
      markAsRead: string;
      setReminder: string;
    };
  };

  // 医生偏好设置
  preferences: {
    practitionerId: string;

    // 关注的疾病类型
    interestedDiseases: string[];

    // 关注的区域
    interestedRegions: string[];

    // 通知频率
    frequency: 'immediate' | 'daily' | 'weekly';

    // 通知渠道偏好
    preferredChannels: string[];
  };
}
```

### 5.6 预警界面设计

```
┌─────────────────────────────────────────────────────────────┐
│  🔔 传染病预警中心                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ 最新预警 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🟠 等级3警告 - 新型流感变异株                          │   │
│  │  发布时间: 2025-11-17 09:30                           │   │
│  │                                                       │   │
│  │  📍 影响区域: 东南亚多国，包括马来西亚                   │   │
│  │  📊 本地病例: 45例（本周新增12例）                      │   │
│  │  📈 趋势: 上升中                                      │   │
│  │                                                       │   │
│  │  🏥 主要症状:                                         │   │
│  │  • 高热（39°C以上）                                   │   │
│  │  • 剧烈头痛                                           │   │
│  │  • 全身肌肉酸痛                                       │   │
│  │  • 咳嗽、咽痛                                         │   │
│  │                                                       │   │
│  │  [查看详情] [查看中医方案] [标记已读]                    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 中医治疗方案速览 ─────────────────────────────────┐   │
│  │                                                       │   │
│  │  📋 方案名称: 新型流感中医诊疗方案（2025版）             │   │
│  │  📅 发布日期: 2025-11-15                               │   │
│  │  🏛️ 来源: 国家中医药管理局                             │   │
│  │                                                       │   │
│  │  ─────────────────────────────────────────────────    │   │
│  │                                                       │   │
│  │  🔹 初期 - 风热犯卫证                                  │   │
│  │                                                       │   │
│  │  症状: 发热，微恶寒，咽红，咳嗽                         │   │
│  │  舌脉: 舌红，苔薄白，脉浮数                            │   │
│  │                                                       │   │
│  │  推荐方剂: 银翘散加减                                  │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ 金银花 15g  连翘 15g   薄荷 6g（后下）        │     │   │
│  │  │ 荆芥 10g   牛蒡子 10g  桔梗 10g  甘草 6g     │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  [一键导入处方] [查看完整方案]                          │   │
│  │                                                       │   │
│  │  ─────────────────────────────────────────────────    │   │
│  │                                                       │   │
│  │  🔹 中期 - 热毒壅肺证                                  │   │
│  │  🔹 重症期 - 内闭外脱证                                │   │
│  │  🔹 恢复期 - 气阴两虚证                                │   │
│  │                                                       │   │
│  │  [展开查看]                                           │   │
│  │                                                       │   │
│  │  ─────────────────────────────────────────────────    │   │
│  │                                                       │   │
│  │  🛡️ 预防方案                                          │   │
│  │                                                       │   │
│  │  预防方: 玉屏风散加板蓝根、贯众                        │   │
│  │  艾灸: 足三里、关元、气海                              │   │
│  │                                                       │   │
│  │  [下载完整PDF] [打印速查卡] [分享给同事]                │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 历史预警 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  日期        疾病          等级   状态                 │   │
│  │  2025-11-10  登革热        🟡2    已读                 │   │
│  │  2025-11-05  手足口病      🔵1    已读                 │   │
│  │  2025-10-28  疟疾          🟡2    已读                 │   │
│  │                                                       │   │
│  │  [查看全部历史预警]                                    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 通知设置 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  关注疾病: [呼吸道传染病] [虫媒传染病] [新发传染病]     │   │
│  │  关注区域: [雪兰莪] [吉隆坡] [全国]                     │   │
│  │  通知方式: ☑ 应用内 ☑ 邮件 ☐ 短信                      │   │
│  │  通知频率: [实时] [每日汇总] [每周汇总]                 │   │
│  │                                                       │   │
│  │  [保存设置]                                           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 知识库在线更新机制

### 6.1 更新架构设计

```typescript
interface KnowledgeBaseUpdateSystem {
  // 知识库模块
  knowledgeBases: {
    // 方剂数据库
    formulas: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
      source: string[];
    };

    // 中药数据库
    herbs: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
      source: string[];
    };

    // 穴位数据库
    acupoints: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
      source: string[];
    };

    // 推拿手法数据库
    tuinaTechniques: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
    };

    // 传染病方案库
    epidemicProtocols: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
    };

    // 现代研究数据库
    modernResearch: {
      version: string;
      lastUpdate: string;
      totalRecords: number;
    };
  };

  // 更新机制
  updateMechanism: {
    // 增量更新
    incrementalUpdate: {
      enabled: boolean;
      diffFormat: 'JSON-Patch' | 'Custom';
      compressionEnabled: boolean;
    };

    // 更新来源
    updateSources: {
      official: {
        // 官方更新服务器
        primary: string;
        backup: string;
        authentication: 'API-Key' | 'OAuth';
      };

      // 可信第三方源
      trusted: {
        name: string;
        endpoint: string;
        contentType: string[];
      }[];
    };

    // 更新验证
    verification: {
      checksum: 'SHA-256';
      signature: 'RSA-2048';
      certificateAuthority: string;
    };
  };
}
```

### 6.2 更新流程

```typescript
interface UpdateProcess {
  // 自动检查更新
  autoCheck: {
    frequency: 'hourly' | 'daily' | 'weekly';
    checkTime: string;          // 检查时间
    bandwidth: 'low' | 'medium' | 'high';
  };

  // 更新包结构
  updatePackage: {
    packageId: string;
    knowledgeBase: string;      // 哪个知识库

    version: {
      from: string;
      to: string;
    };

    changes: {
      added: {
        count: number;
        items: any[];
      };
      modified: {
        count: number;
        items: any[];
      };
      deleted: {
        count: number;
        itemIds: string[];
      };
    };

    size: number;               // 字节
    checksum: string;
    signature: string;

    releaseNotes: {
      summary: string;
      highlights: string[];
      references: string[];
    };
  };

  // 更新执行
  updateExecution: {
    steps: [
      'download',
      'verify',
      'backup',
      'apply',
      'validate',
      'cleanup'
    ];

    rollback: {
      enabled: boolean;
      keepVersions: number;
    };

    // 执行选项
    options: {
      immediateApply: boolean;
      requireApproval: boolean;
      scheduledTime?: string;
    };
  };
}
```

### 6.3 版本管理

```typescript
interface VersionControl {
  // 版本历史
  versionHistory: {
    knowledgeBase: string;
    versions: {
      version: string;
      releaseDate: string;
      changes: string;
      status: 'current' | 'previous' | 'archived';
    }[];
  };

  // 回滚能力
  rollback: {
    // 可回滚的版本
    availableVersions: string[];

    // 回滚操作
    performRollback: (targetVersion: string) => {
      success: boolean;
      message: string;
      affectedRecords: number;
    };
  };

  // 自定义内容保护
  customContent: {
    // 用户自定义的方剂/穴位等
    preserveOnUpdate: boolean;
    conflictResolution: 'keep-local' | 'keep-remote' | 'merge' | 'ask';
  };
}
```

### 6.4 更新内容示例

```json
{
  "packageId": "herbs-update-2025-11-01",
  "knowledgeBase": "herbs",
  "version": {
    "from": "3.5.2",
    "to": "3.6.0"
  },
  "changes": {
    "added": {
      "count": 15,
      "items": [
        {
          "herbId": "HRB-2025-001",
          "name": "新发现药用植物",
          "category": "清热药",
          "modernResearch": "2025年最新研究..."
        }
      ]
    },
    "modified": {
      "count": 42,
      "items": [
        {
          "herbId": "HRB-0001",
          "field": "modernResearch",
          "reason": "新增2025年临床研究数据",
          "oldValue": "...",
          "newValue": "..."
        },
        {
          "herbId": "HRB-0156",
          "field": "interactions",
          "reason": "发现新的药物相互作用",
          "oldValue": [],
          "newValue": ["与华法林有相互作用"]
        }
      ]
    },
    "deleted": {
      "count": 0,
      "itemIds": []
    }
  },
  "releaseNotes": {
    "summary": "本次更新主要包含2025年最新中药研究成果",
    "highlights": [
      "新增15种药用植物数据",
      "更新42种中药的现代研究信息",
      "完善药物相互作用数据"
    ],
    "references": [
      "中国药典2025年版",
      "Journal of Ethnopharmacology 2025"
    ]
  }
}
```

---

## 7. 自动更新提醒系统

### 7.1 提醒类型

```typescript
interface UpdateReminderSystem {
  // 提醒类型
  reminderTypes: {
    // 知识库更新
    knowledgeBaseUpdate: {
      trigger: 'new-version-available';
      priority: 'normal' | 'high';
      content: {
        database: string;
        currentVersion: string;
        newVersion: string;
        highlights: string[];
      };
    };

    // 新发传染病方案
    epidemicProtocol: {
      trigger: 'new-protocol-published';
      priority: 'high';
      content: {
        disease: string;
        protocolName: string;
        source: string;
        publishDate: string;
      };
    };

    // 临床指南更新
    guidelineUpdate: {
      trigger: 'guideline-updated';
      priority: 'normal';
      content: {
        guidelineName: string;
        changes: string[];
        effectiveDate: string;
      };
    };

    // 药物安全警告
    drugSafetyAlert: {
      trigger: 'safety-alert-issued';
      priority: 'high';
      content: {
        drug: string;
        alertType: 'recall' | 'interaction' | 'contraindication';
        details: string;
        action: string;
      };
    };

    // 系统更新
    systemUpdate: {
      trigger: 'system-update-available';
      priority: 'normal';
      content: {
        currentVersion: string;
        newVersion: string;
        features: string[];
        bugFixes: string[];
      };
    };
  };

  // 提醒方式
  notificationMethods: {
    inAppNotification: {
      badge: boolean;
      popup: boolean;
      sound: boolean;
    };

    email: {
      enabled: boolean;
      digest: 'immediate' | 'daily' | 'weekly';
    };

    sms: {
      enabled: boolean;
      onlyForHigh: boolean;
    };

    pushNotification: {
      enabled: boolean;
    };
  };
}
```

### 7.2 智能提醒调度

```typescript
interface SmartReminderScheduling {
  // 智能调度规则
  scheduling: {
    // 避免打扰
    quietHours: {
      enabled: boolean;
      start: string;            // "22:00"
      end: string;              // "07:00"
      exceptEmergency: boolean;
    };

    // 工作时间优先
    workingHours: {
      start: string;
      end: string;
      preferredTime: string;
    };

    // 批量发送
    batching: {
      enabled: boolean;
      interval: string;         // "4h"
      maxPerBatch: number;
    };

    // 重要性排序
    prioritization: {
      highPriority: 'immediate';
      normalPriority: 'batched';
      lowPriority: 'digest';
    };
  };

  // 用户行为学习
  userBehaviorLearning: {
    // 学习用户习惯
    trackInteractions: boolean;

    // 调整提醒时间
    optimizeTimimg: boolean;

    // 调整提醒频率
    adjustFrequency: boolean;
  };
}
```

### 7.3 提醒管理界面

```
┌─────────────────────────────────────────────────────────────┐
│  📢 更新提醒中心                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ 待处理提醒 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🔴 高优先级                                          │   │
│  │  ──────────────────────────────────────────────────   │   │
│  │                                                       │   │
│  │  💊 药物安全警告                     2025-11-17 08:00  │   │
│  │  何首乌新增肝毒性警告，建议限制剂量                      │   │
│  │  [查看详情] [已知悉]                                   │   │
│  │                                                       │   │
│  │  🦠 新传染病方案发布                 2025-11-16 15:30  │   │
│  │  新型流感中医诊疗方案（2025版）已发布                    │   │
│  │  [下载方案] [已知悉]                                   │   │
│  │                                                       │   │
│  │  🟡 普通优先级                                        │   │
│  │  ──────────────────────────────────────────────────   │   │
│  │                                                       │   │
│  │  📚 中药数据库更新可用               2025-11-15 10:00  │   │
│  │  版本 3.5.2 → 3.6.0                                   │   │
│  │  新增15种中药，更新42种现代研究数据                      │   │
│  │  [查看更新内容] [立即更新] [稍后提醒]                    │   │
│  │                                                       │   │
│  │  📚 方剂数据库更新可用               2025-11-14 09:00  │   │
│  │  版本 2.8.1 → 2.9.0                                   │   │
│  │  新增古方32首，更新配伍研究                             │   │
│  │  [查看更新内容] [立即更新] [稍后提醒]                    │   │
│  │                                                       │   │
│  │  📍 穴位数据库更新可用               2025-11-12 11:00  │   │
│  │  版本 1.5.0 → 1.6.0                                   │   │
│  │  更新穴位图片，新增3D模型                               │   │
│  │  [查看更新内容] [立即更新] [稍后提醒]                    │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 当前版本状态 ───────────────────────────────────────┐   │
│  │                                                       │   │
│  │  数据库            当前版本   最新版本   状态          │   │
│  │  ─────────────────────────────────────────────────    │   │
│  │  中药数据库        3.5.2     3.6.0     ⚠️ 有更新      │   │
│  │  方剂数据库        2.8.1     2.9.0     ⚠️ 有更新      │   │
│  │  穴位数据库        1.5.0     1.6.0     ⚠️ 有更新      │   │
│  │  传染病方案库      2025.11   2025.11   ✅ 最新        │   │
│  │  推拿手法库        1.2.0     1.2.0     ✅ 最新        │   │
│  │                                                       │   │
│  │  [全部更新] [检查更新]                                 │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 提醒设置 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  通知方式:                                            │   │
│  │  ☑ 应用内通知   ☑ 邮件通知   ☐ 短信通知               │   │
│  │                                                       │   │
│  │  邮件摘要: [每日] ▼                                   │   │
│  │                                                       │   │
│  │  免打扰时段: [22:00] - [07:00]                        │   │
│  │  (紧急提醒除外)                                       │   │
│  │                                                       │   │
│  │  自动更新:                                            │   │
│  │  ☑ 知识库自动更新（需管理员审批）                       │   │
│  │  ☐ 静默更新（无需确认）                                │   │
│  │                                                       │   │
│  │  [保存设置]                                           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 更新历史 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  2025-11-10  中药数据库 3.5.1 → 3.5.2  ✅ 成功        │   │
│  │  2025-11-08  穴位数据库 1.4.5 → 1.5.0  ✅ 成功        │   │
│  │  2025-11-05  方剂数据库 2.8.0 → 2.8.1  ✅ 成功        │   │
│  │                                                       │   │
│  │  [查看完整历史]                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. 数据库设计

### 8.1 AI相关表结构

```sql
-- AI诊断记录表
CREATE TABLE ai_diagnosis_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id UUID REFERENCES visits(visit_id),

    -- 四诊AI分析结果
    wang_zhen_analysis JSONB,      -- 望诊分析
    wen_zhen_analysis JSONB,       -- 闻诊分析
    wen_zhen_questions JSONB,      -- 问诊分析
    qie_zhen_analysis JSONB,       -- 切诊分析

    -- 病因病机分析
    etiology_analysis JSONB,       -- 病因分析
    pathogenesis_analysis JSONB,   -- 病机分析
    syndrome_analysis JSONB,       -- 证型分析

    -- AI建议
    treatment_suggestions JSONB,   -- 治疗建议

    -- 医生采纳情况
    accepted_suggestions JSONB,    -- 采纳的建议
    modified_suggestions JSONB,    -- 修改的建议
    rejected_suggestions JSONB,    -- 拒绝的建议

    -- 元数据
    ai_model_version VARCHAR(50),
    confidence_score DECIMAL(5,2),
    processing_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI处方推荐记录表
CREATE TABLE ai_prescription_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id UUID REFERENCES visits(visit_id),

    -- 输入信息
    syndrome VARCHAR(200),
    symptoms TEXT[],
    patient_profile JSONB,

    -- AI推荐
    primary_formula JSONB,         -- 主方推荐
    alternative_formulas JSONB,    -- 备选方
    modifications JSONB,           -- 加减建议
    safety_check_results JSONB,    -- 安全检查结果

    -- 医生处理
    final_prescription JSONB,      -- 最终处方
    ai_suggestions_used BOOLEAN,
    modification_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI穴位推荐记录表
CREATE TABLE ai_acupoint_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id UUID REFERENCES visits(visit_id),

    -- 输入信息
    syndrome VARCHAR(200),
    symptoms TEXT[],
    treatment_goal TEXT,

    -- AI推荐
    primary_points JSONB,          -- 主穴
    secondary_points JSONB,        -- 配穴
    symptom_additions JSONB,       -- 随症加减
    classic_references JSONB,      -- 经典依据

    -- 医生处理
    final_points JSONB,
    treatment_record JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 知识库版本管理表
CREATE TABLE knowledge_base_versions (
    version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base VARCHAR(50) NOT NULL,  -- formulas, herbs, acupoints, etc.
    version VARCHAR(20) NOT NULL,

    -- 版本信息
    release_date TIMESTAMP,
    release_notes TEXT,
    changes_summary JSONB,

    -- 状态
    status VARCHAR(20) DEFAULT 'available',  -- available, installed, archived
    installed_at TIMESTAMP,

    -- 文件信息
    package_url TEXT,
    package_size BIGINT,
    checksum VARCHAR(64),
    signature TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 更新日志表
CREATE TABLE knowledge_base_update_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base VARCHAR(50),

    -- 版本变更
    from_version VARCHAR(20),
    to_version VARCHAR(20),

    -- 更新详情
    changes JSONB,
    records_added INTEGER,
    records_modified INTEGER,
    records_deleted INTEGER,

    -- 状态
    status VARCHAR(20),  -- pending, in_progress, completed, failed, rolled_back
    error_message TEXT,

    -- 执行信息
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    executed_by UUID REFERENCES users(user_id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 传染病预警表
CREATE TABLE epidemic_alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 疾病信息
    disease_name VARCHAR(200),
    pathogen VARCHAR(200),

    -- 预警信息
    alert_level INTEGER,  -- 1-4
    alert_type VARCHAR(50),

    -- 流行病学数据
    affected_regions TEXT[],
    case_count INTEGER,
    fatality_rate DECIMAL(5,2),
    trend VARCHAR(20),

    -- 临床信息
    clinical_features JSONB,

    -- 中医方案
    tcm_protocol_id UUID,
    tcm_protocol_summary TEXT,

    -- 状态
    status VARCHAR(20) DEFAULT 'active',

    -- 来源
    source VARCHAR(100),
    source_url TEXT,
    published_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 中医传染病治疗方案表
CREATE TABLE tcm_epidemic_protocols (
    protocol_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 方案信息
    disease_name VARCHAR(200),
    protocol_name VARCHAR(300),
    version VARCHAR(20),

    -- 来源
    issuing_authority VARCHAR(200),
    publish_date DATE,

    -- 方案内容
    tcm_understanding JSONB,       -- 中医认识
    treatment_by_stage JSONB,      -- 分期治疗
    prevention JSONB,              -- 预防方案

    -- 附件
    full_document_url TEXT,
    quick_reference_url TEXT,

    -- 状态
    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户提醒偏好表
CREATE TABLE user_notification_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),

    -- 关注内容
    interested_diseases TEXT[],
    interested_regions TEXT[],
    interested_updates TEXT[],

    -- 通知渠道
    channels JSONB,

    -- 时间设置
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    digest_frequency VARCHAR(20),

    -- 自动更新设置
    auto_update_enabled BOOLEAN DEFAULT FALSE,
    require_approval BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 提醒发送记录表
CREATE TABLE notification_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),

    -- 提醒内容
    notification_type VARCHAR(50),
    title VARCHAR(300),
    content TEXT,
    priority VARCHAR(20),

    -- 发送渠道
    channel VARCHAR(20),

    -- 状态
    status VARCHAR(20),  -- sent, delivered, read, failed
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,

    -- 用户操作
    user_action VARCHAR(50),  -- clicked, dismissed, snoozed
    action_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_ai_diagnosis_visit ON ai_diagnosis_records(visit_id);
CREATE INDEX idx_ai_prescription_visit ON ai_prescription_records(visit_id);
CREATE INDEX idx_kb_versions_base ON knowledge_base_versions(knowledge_base);
CREATE INDEX idx_epidemic_alerts_status ON epidemic_alerts(status, alert_level);
CREATE INDEX idx_notification_user ON notification_logs(user_id, status);
```

### 8.2 穴位数据库完整表结构

```sql
-- 穴位主表
CREATE TABLE acupoints (
    acupoint_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 名称
    name_chinese VARCHAR(50) NOT NULL,
    name_pinyin VARCHAR(100),
    name_english VARCHAR(100),
    code VARCHAR(20),             -- 国际代码如 LI4
    alternative_names TEXT[],

    -- 归经
    meridian_id UUID REFERENCES meridians(meridian_id),
    point_type VARCHAR(50),       -- 经穴/经外奇穴
    sequence_number INTEGER,

    -- 特定穴属性
    special_point_types TEXT[],   -- 五输穴/原穴/络穴/郗穴等

    -- 定位
    location_description TEXT,
    easy_location_method TEXT,

    -- 解剖
    anatomy_region VARCHAR(100),
    anatomy_muscles TEXT[],
    anatomy_nerves TEXT[],
    anatomy_vessels TEXT[],

    -- 3D坐标
    coordinate_x DECIMAL(10,4),
    coordinate_y DECIMAL(10,4),
    coordinate_z DECIMAL(10,4),
    body_part VARCHAR(50),

    -- 功效主治
    functions TEXT[],
    indications TEXT[],
    indications_by_system JSONB,
    special_actions TEXT[],

    -- 操作
    needling_angle VARCHAR(50),
    needling_depth VARCHAR(50),
    needling_sensation TEXT,
    needling_cautions TEXT[],

    moxibustion_suitable BOOLEAN,
    moxibustion_method TEXT,

    cupping_suitable BOOLEAN,

    -- 配伍
    common_combinations JSONB,

    -- 禁忌
    contraindications TEXT[],

    -- 现代研究
    modern_research JSONB,

    -- 图片
    image_location VARCHAR(500),
    image_anatomy VARCHAR(500),
    image_needling VARCHAR(500),
    video_url VARCHAR(500),

    -- 数据来源和版本
    data_source VARCHAR(100),
    version VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 经络表
CREATE TABLE meridians (
    meridian_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name_chinese VARCHAR(50),
    name_pinyin VARCHAR(100),
    name_english VARCHAR(100),
    abbreviation VARCHAR(10),

    meridian_type VARCHAR(50),    -- 正经/奇经
    yin_yang VARCHAR(10),

    -- 循行
    pathway_description TEXT,

    -- 主治
    main_indications TEXT[],

    -- 图片
    pathway_image VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 穴位配伍表
CREATE TABLE acupoint_combinations (
    combination_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    acupoint_id UUID REFERENCES acupoints(acupoint_id),
    partner_acupoint_id UUID REFERENCES acupoints(acupoint_id),

    combined_effect TEXT,
    indication TEXT,
    classic_source VARCHAR(200),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 穴位图片资源表
CREATE TABLE acupoint_images (
    image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    acupoint_id UUID REFERENCES acupoints(acupoint_id),

    image_type VARCHAR(50),       -- location/anatomy/needling/moxibustion
    image_url VARCHAR(500),
    thumbnail_url VARCHAR(500),

    description TEXT,

    -- 图片元数据
    width INTEGER,
    height INTEGER,
    file_size BIGINT,
    format VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3D模型资源表
CREATE TABLE body_3d_models (
    model_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    model_type VARCHAR(50),       -- male/female/child
    model_url VARCHAR(500),
    format VARCHAR(20),           -- glb/obj

    -- 特性
    features JSONB,

    version VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 9. 系统架构

### 9.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI增强中医诊疗系统架构                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─ 表示层 ──────────────────────────────────────────────────────────┐  │
│  │  Web应用(React)  │  移动应用(React Native)  │  桌面应用(Electron)   │  │
│  └───────────────────────────────┬───────────────────────────────────┘  │
│                                  │                                       │
│  ┌─ API网关层 ───────────────────┴───────────────────────────────────┐  │
│  │  Kong/AWS API Gateway                                              │  │
│  │  • 认证/授权  • 限流  • 日志  • 路由                                 │  │
│  └───────────────────────────────┬───────────────────────────────────┘  │
│                                  │                                       │
│  ┌─ 微服务层 ────────────────────┴───────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │  │
│  │  │ 患者服务    │ │ 诊疗服务    │ │ 处方服务    │ │ 针灸服务    │      │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │  │
│  │                                                                    │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │  │
│  │  │ 预约服务    │ │ 报告服务    │ │ 通知服务    │ │ 计费服务    │      │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │  │
│  │                                                                    │  │
│  └───────────────────────────────┬───────────────────────────────────┘  │
│                                  │                                       │
│  ┌─ AI服务层 ────────────────────┴───────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐    │  │
│  │  │ AI诊断引擎       │  │ AI开方引擎       │  │ AI针灸引擎       │    │  │
│  │  │ • 四诊分析       │  │ • 方剂推荐       │  │ • 穴位推荐       │    │  │
│  │  │ • 病机分析       │  │ • 安全检查       │  │ • 治疗方案       │    │  │
│  │  │ • 辨证建议       │  │ • 加减建议       │  │ • 可视化         │    │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘    │  │
│  │                                                                    │  │
│  │  ┌─────────────────┐  ┌─────────────────┐                         │  │
│  │  │ 传染病监测引擎    │  │ 知识库更新引擎    │                         │  │
│  │  │ • 数据采集       │  │ • 版本管理       │                         │  │
│  │  │ • 预警生成       │  │ • 增量更新       │                         │  │
│  │  │ • 方案推送       │  │ • 提醒调度       │                         │  │
│  │  └─────────────────┘  └─────────────────┘                         │  │
│  │                                                                    │  │
│  └───────────────────────────────┬───────────────────────────────────┘  │
│                                  │                                       │
│  ┌─ 知识图谱层 ──────────────────┴───────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │  │
│  │  │ 中医知识图谱  │  │ 医学本体库   │  │ 推理引擎     │                │  │
│  │  │ Neo4j       │  │ OWL/RDF    │  │ SWRL       │                │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                │  │
│  │                                                                    │  │
│  └───────────────────────────────┬───────────────────────────────────┘  │
│                                  │                                       │
│  ┌─ 数据层 ──────────────────────┴───────────────────────────────────┐  │
│  │                                                                    │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │  │
│  │  │ PostgreSQL │ │ MongoDB    │ │ Redis      │ │ MinIO      │      │  │
│  │  │ 业务数据    │ │ 文档/日志   │ │ 缓存/会话   │ │ 文件存储    │      │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │  │
│  │                                                                    │  │
│  │  ┌────────────────────────────────────────────────────────┐       │  │
│  │  │ 可更新知识库                                             │       │  │
│  │  │ • 方剂库  • 中药库  • 穴位库  • 推拿库  • 传染病方案库     │       │  │
│  │  └────────────────────────────────────────────────────────┘       │  │
│  │                                                                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─ 外部集成 ────────────────────────────────────────────────────────┐  │
│  │  WHO API │ MOH Malaysia │ 国家中医药管理局 │ 医学文献数据库           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.2 AI服务技术选型

```typescript
interface AITechnologyStack {
  // 机器学习框架
  mlFrameworks: {
    primary: 'PyTorch';
    secondary: 'TensorFlow';
    serving: 'TorchServe' | 'TF Serving';
  };

  // NLP处理
  nlp: {
    framework: 'Hugging Face Transformers';
    models: {
      chineseBERT: 'bert-base-chinese';
      medicalNER: 'custom-tcm-ner';
      textGeneration: 'custom-tcm-gpt';
    };
  };

  // 计算机视觉（舌诊、面诊）
  computerVision: {
    framework: 'PyTorch + torchvision';
    models: {
      tongueClassification: 'custom-tongue-classifier';
      faceAnalysis: 'custom-face-analyzer';
    };
  };

  // 知识图谱
  knowledgeGraph: {
    database: 'Neo4j';
    queryLanguage: 'Cypher';
    embeddingModel: 'TransE' | 'RotatE';
  };

  // 推理引擎
  reasoningEngine: {
    ruleEngine: 'Drools';
    probabilisticReasoning: 'ProbLog';
  };

  // 向量数据库（相似病例检索）
  vectorDatabase: {
    engine: 'Milvus' | 'Pinecone';
    dimension: 768;
    indexType: 'IVF_FLAT';
  };

  // 部署
  deployment: {
    containerization: 'Docker';
    orchestration: 'Kubernetes';
    gpuSupport: 'NVIDIA CUDA';
    modelRegistry: 'MLflow';
  };
}
```

### 9.3 安全架构

```typescript
interface SecurityArchitecture {
  // 数据安全
  dataSecurity: {
    // 加密
    encryption: {
      atRest: 'AES-256';
      inTransit: 'TLS 1.3';
      fieldLevel: ['patient_name', 'nric', 'medical_records'];
    };

    // 数据脱敏
    masking: {
      pii: boolean;
      phi: boolean;
      logs: boolean;
    };

    // 备份
    backup: {
      frequency: 'daily';
      retention: '7 years';
      encryption: boolean;
      offsite: boolean;
    };
  };

  // 访问控制
  accessControl: {
    authentication: 'OAuth 2.0 + JWT';
    authorization: 'RBAC + ABAC';
    mfa: 'TOTP / SMS';
    sessionTimeout: '30 minutes';
  };

  // AI模型安全
  aiSecurity: {
    // 模型保护
    modelProtection: {
      encryption: boolean;
      accessControl: boolean;
      versioning: boolean;
    };

    // 输入验证
    inputValidation: {
      sanitization: boolean;
      adversarialDetection: boolean;
    };

    // 输出审计
    outputAudit: {
      logging: boolean;
      humanReview: boolean;
    };
  };

  // 合规
  compliance: {
    pdpa: boolean;
    hipaa: boolean;
    iso27001: boolean;
  };
}
```

---

## 10. 实施计划

### 10.1 阶段规划

```
阶段1: 基础设施和核心功能（第1-3月）
├── 系统架构搭建
├── 基础数据库设计和实现
├── 用户认证和授权
├── 患者管理模块
└── 基本诊疗记录

阶段2: AI基础功能（第4-6月）
├── AI病案助手
│   ├── 四诊智能采集
│   ├── 病因病机分析
│   └── 辨证建议
├── AI开方助手
│   ├── 方剂推荐引擎
│   ├── 安全检查系统
│   └── 加减建议
└── 中医知识图谱基础

阶段3: 针灸推拿和可视化（第7-8月）
├── 穴位数据库完善
├── 3D人体模型集成
├── AI穴位推荐
├── 推拿手法数据库
└── 治疗记录可视化

阶段4: 知识库更新系统（第9月）
├── 知识库版本管理
├── 增量更新机制
├── 更新提醒系统
└── 自动/手动更新流程

阶段5: 传染病监测系统（第10月）
├── 数据源集成
├── 监测和预警引擎
├── 中医方案推送
└── 通知系统完善

阶段6: 测试和优化（第11-12月）
├── 集成测试
├── 用户验收测试
├── 性能优化
├── 安全审计
└── 合规认证

阶段7: 部署和培训（第13月）
├── 生产环境部署
├── 数据迁移
├── 用户培训
└── 上线支持
```

### 10.2 预算估算

| 类别 | 项目 | 预算 (RM) |
|------|------|-----------|
| **开发** | 后端开发（含AI）| 350,000 |
| | 前端开发 | 180,000 |
| | AI模型开发和训练 | 200,000 |
| | 3D模型和图片资源 | 80,000 |
| | 测试和QA | 100,000 |
| **基础设施** | 云服务（首年）| 120,000 |
| | AI计算资源（GPU）| 80,000 |
| | 知识库授权 | 50,000 |
| **其他** | 安全审计和认证 | 60,000 |
| | 培训和文档 | 40,000 |
| | 项目管理 | 80,000 |
| **总计** | | **1,340,000** |

### 10.3 团队配置

```
项目经理 x 1
产品经理 x 1
后端开发 x 4
前端开发 x 3
AI/ML工程师 x 3
中医领域专家 x 2
UI/UX设计师 x 1
DevOps工程师 x 1
QA工程师 x 2
安全工程师 x 1

总计: 19人
```

### 10.4 风险管理

| 风险 | 影响 | 可能性 | 缓解措施 |
|------|------|--------|----------|
| AI模型准确率不达标 | 高 | 中 | 增加训练数据，专家审核，持续优化 |
| 知识库更新延迟 | 中 | 中 | 多数据源，自动化监测 |
| 中医专家资源不足 | 高 | 低 | 提前签约，远程咨询 |
| 法规合规风险 | 高 | 低 | 法律顾问，持续监测 |
| 数据安全事件 | 高 | 低 | 多层防护，定期审计 |

---

## 附录

### A. 中医术语AI识别标准

系统需要识别和理解以下中医术语类别：

1. **证型术语** - 300+ 常见证型
2. **症状术语** - 1000+ 症状描述
3. **舌象术语** - 100+ 舌诊描述
4. **脉象术语** - 28脉及其变化
5. **方剂名称** - 2000+ 常用方剂
6. **中药名称** - 500+ 常用中药
7. **穴位名称** - 361经穴 + 常用奇穴

### B. AI模型评估指标

| 功能 | 指标 | 目标值 |
|------|------|--------|
| 证型推荐 | Top-3准确率 | ≥85% |
| 方剂推荐 | Top-5准确率 | ≥80% |
| 穴位推荐 | 专家一致率 | ≥75% |
| 安全检查 | 召回率 | ≥99% |
| 舌诊分析 | 分类准确率 | ≥90% |

### C. 数据更新频率

| 知识库 | 检查频率 | 来源 |
|--------|----------|------|
| 中药数据库 | 每周 | 药典/研究论文 |
| 方剂数据库 | 每周 | 临床指南/研究 |
| 穴位数据库 | 每月 | 国际标准 |
| 传染病方案 | 实时 | 卫生部/WHO |
| 药物相互作用 | 每日 | 药物数据库 |

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0 | 2025-11-17 | 初始版本 |

---

**文档结束**
