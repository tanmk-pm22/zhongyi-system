# 语音识别、多语言翻译与现代医学集成系统

## 版本: 1.0
## 日期: 2025年11月17日

---

## 目录

1. [系统概述](#1-系统概述)
2. [语音转文字AI系统](#2-语音转文字ai系统)
3. [多语言支持系统](#3-多语言支持系统)
4. [AI翻译功能](#4-ai翻译功能)
5. [现代医学治疗方案集成](#5-现代医学治疗方案集成)
6. [数据库设计](#6-数据库设计)
7. [API接口设计](#7-api接口设计)
8. [界面设计](#8-界面设计)
9. [技术选型](#9-技术选型)
10. [实施计划](#10-实施计划)

---

## 1. 系统概述

### 1.1 功能目标

为AI增强中医诊疗系统添加以下核心功能：

1. **语音转文字** - 医生可通过语音输入病案信息，系统自动转换为文字
2. **多语言支持** - 支持中文、英文、马来文、粤语、闽南语等多种语言
3. **AI翻译** - 实时翻译医学术语和病案内容
4. **现代医学集成** - 补充西医诊断、检查、治疗方案

### 1.2 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    语音·翻译·现代医学集成系统                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ 语音处理层 ────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🎤 语音输入 → ASR引擎 → 文字输出                      │   │
│  │                                                       │   │
│  │  支持：普通话/粤语/闽南语/英语/马来语                    │   │
│  │  专业：中医术语识别模型                                 │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌─ AI翻译层 ─────────────┴────────────────────────────┐   │
│  │                                                       │   │
│  │  中文 ⟷ 英文 ⟷ 马来文 ⟷ 印尼文                        │   │
│  │                                                       │   │
│  │  医学术语库 │ 中医专业词典 │ 上下文理解                  │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                           │                                  │
│  ┌─ 现代医学集成层 ────────┴────────────────────────────┐   │
│  │                                                       │   │
│  │  西医诊断(ICD-10) │ 检查项目 │ 西药处方 │ 治疗指南      │   │
│  │                                                       │   │
│  │  中西医对照 │ 联合治疗方案 │ 循证医学数据库              │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 语音转文字AI系统

### 2.1 功能设计

```typescript
interface SpeechToTextSystem {
  // 核心功能
  features: {
    // 实时语音识别
    realTimeRecognition: {
      streaming: true;
      latency: '<500ms';
      continuous: true;
    };

    // 离线识别（可选）
    offlineRecognition: {
      enabled: boolean;
      languages: ['zh-CN', 'en'];
    };

    // 医学术语增强
    medicalEnhancement: {
      tcmTerminology: true;      // 中医术语
      westernMedicine: true;     // 西医术语
      drugNames: true;           // 药名
      anatomyTerms: true;        // 解剖术语
    };

    // 方言支持
    dialectSupport: {
      cantonese: true;           // 粤语
      hokkien: true;             // 闽南语
      hakka: boolean;            // 客家话
      teochew: boolean;          // 潮州话
    };
  };

  // 输入模式
  inputModes: {
    // 按住说话
    pushToTalk: {
      buttonHold: true;
      autoStop: true;
    };

    // 连续听写
    continuousDictation: {
      voiceActivityDetection: true;
      autoCommands: ['句号', '逗号', '换行', '删除'];
    };

    // 命令模式
    voiceCommands: {
      enabled: true;
      commands: [
        '下一项',
        '保存',
        '清空',
        '重新输入'
      ];
    };
  };
}
```

### 2.2 语音识别引擎

```typescript
interface ASREngine {
  // 多引擎支持
  engines: {
    // 主引擎：云端API
    primary: {
      provider: 'Azure Speech' | 'Google Cloud Speech' | 'Alibaba Cloud';
      features: {
        customModel: true;        // 自定义语言模型
        realTime: true;
        multiLanguage: true;
      };
    };

    // 备用引擎：本地
    fallback: {
      provider: 'Vosk' | 'Mozilla DeepSpeech';
      features: {
        offline: true;
        privacy: 'high';
      };
    };
  };

  // 中医专业模型
  tcmModel: {
    // 自定义词汇表
    customVocabulary: {
      syndromes: string[];       // 证型名称
      herbs: string[];           // 中药名
      acupoints: string[];       // 穴位名
      formulas: string[];        // 方剂名
      symptoms: string[];        // 症状描述
    };

    // 领域适应
    domainAdaptation: {
      trainingData: 'TCM clinical records';
      optimization: 'Medical terminology';
    };
  };

  // 后处理
  postProcessing: {
    // 标点符号
    punctuation: {
      auto: true;
      voice: true;              // 语音输入标点
    };

    // 数字格式化
    numberFormatting: {
      dosages: true;            // "六克" → "6g"
      measurements: true;
    };

    // 医学术语规范化
    termNormalization: {
      standardize: true;        // 统一术语
      expandAbbreviations: true; // 展开缩写
    };
  };
}
```

### 2.3 语音输入字段配置

```typescript
interface VoiceInputFields {
  // 支持语音输入的字段
  enabledFields: {
    // 病案记录
    medicalRecord: {
      chiefComplaint: true;      // 主诉
      presentIllness: true;      // 现病史
      pastHistory: true;         // 既往史
      personalHistory: true;     // 个人史
      familyHistory: true;       // 家族史
    };

    // 四诊信息
    fourDiagnosis: {
      inspection: true;          // 望诊
      auscultation: true;        // 闻诊
      inquiry: true;             // 问诊
      palpation: true;           // 切诊
    };

    // 诊断
    diagnosis: {
      tcmDiagnosis: true;        // 中医诊断
      westernDiagnosis: true;    // 西医诊断
      syndrome: true;            // 证型
    };

    // 处方
    prescription: {
      herbNotes: true;           // 中药备注
      usageInstructions: true;   // 用法说明
    };

    // 治疗记录
    treatment: {
      acupunctureNotes: true;    // 针灸记录
      tuinaNotes: true;          // 推拿记录
      progressNotes: true;       // 病程记录
    };
  };

  // 字段配置
  fieldConfig: {
    fieldId: string;
    label: string;
    voiceEnabled: boolean;
    language: string;
    maxLength?: number;
    template?: string;           // 语音输入模板
  };
}
```

### 2.4 语音命令系统

```typescript
interface VoiceCommandSystem {
  // 导航命令
  navigation: {
    '下一项': 'moveToNextField',
    '上一项': 'moveToPreviousField',
    '跳到诊断': 'jumpToField:diagnosis',
    '跳到处方': 'jumpToField:prescription',
  };

  // 编辑命令
  editing: {
    '删除': 'deleteLastWord',
    '全部删除': 'clearField',
    '撤销': 'undo',
    '重做': 'redo',
  };

  // 标点命令
  punctuation: {
    '句号': '。',
    '逗号': '，',
    '问号': '？',
    '感叹号': '！',
    '冒号': '：',
    '换行': '\n',
  };

  // 系统命令
  system: {
    '保存': 'saveRecord',
    '提交': 'submitRecord',
    '暂停': 'pauseRecording',
    '继续': 'resumeRecording',
  };

  // 医学快捷命令
  medical: {
    '生命体征正常': '体温36.5℃，脉搏72次/分，呼吸18次/分，血压120/80mmHg',
    '舌象正常': '舌淡红，苔薄白',
    '脉象正常': '脉和缓有力',
  };
}
```

---

## 3. 多语言支持系统

### 3.1 支持的语言

```typescript
interface LanguageSupport {
  // 系统界面语言
  interfaceLanguages: {
    'zh-CN': '简体中文',
    'zh-TW': '繁体中文',
    'en': 'English',
    'ms': 'Bahasa Melayu',
    'id': 'Bahasa Indonesia',
    'ta': 'தமிழ்',           // 泰米尔语
  };

  // 语音识别语言
  speechRecognitionLanguages: {
    'zh-CN': '普通话',
    'zh-HK': '粤语',
    'zh-TW': '国语（台湾）',
    'nan': '闽南语',
    'en-US': 'English (US)',
    'en-GB': 'English (UK)',
    'ms-MY': 'Bahasa Melayu',
  };

  // 医学术语语言
  medicalTerminologyLanguages: {
    'zh': '中文医学术语',
    'en': 'English Medical Terms',
    'la': 'Latin (Anatomical)',
  };
}
```

### 3.2 多语言内容管理

```typescript
interface MultilingualContent {
  // 中医术语多语言
  tcmTerms: {
    // 证型
    syndromes: {
      id: string;
      translations: {
        'zh-CN': string;       // 肝气郁结
        'zh-TW': string;       // 肝氣鬱結
        'en': string;          // Liver Qi Stagnation
        'ms': string;          // Kesesakan Qi Hati
        pinyin: string;        // Gān Qì Yù Jié
      };
    };

    // 中药
    herbs: {
      id: string;
      translations: {
        'zh-CN': string;       // 当归
        'en': string;          // Angelica sinensis
        'la': string;          // Radix Angelicae Sinensis
        'ms': string;          // Akar Angelica
        pinyin: string;        // Dāng Guī
      };
    };

    // 穴位
    acupoints: {
      id: string;
      translations: {
        'zh-CN': string;       // 足三里
        'en': string;          // Zusanli / ST36
        'ms': string;          // Zu San Li
        pinyin: string;        // Zú Sān Lǐ
      };
    };
  };

  // 界面文本
  uiStrings: {
    key: string;
    translations: {
      [languageCode: string]: string;
    };
  };

  // 报告模板
  reportTemplates: {
    templateId: string;
    language: string;
    content: string;
  };
}
```

### 3.3 语言切换机制

```typescript
interface LanguageSwitching {
  // 用户偏好
  userPreferences: {
    interfaceLanguage: string;
    inputLanguage: string;
    outputLanguage: string;
    speechLanguage: string;
  };

  // 自动检测
  autoDetection: {
    // 语音语言检测
    speechLanguage: {
      enabled: true;
      confidence: number;
    };

    // 文本语言检测
    textLanguage: {
      enabled: true;
      fallback: 'zh-CN';
    };
  };

  // 实时切换
  realTimeSwitching: {
    // 支持会话中切换语言
    midSession: true;

    // 混合语言输入
    mixedLanguage: {
      enabled: true;
      primary: string;
      secondary: string[];
    };
  };
}
```

---

## 4. AI翻译功能

### 4.1 翻译系统架构

```typescript
interface TranslationSystem {
  // 翻译引擎
  engines: {
    // 主引擎
    primary: {
      provider: 'DeepL' | 'Google Translate' | 'Azure Translator';
      features: {
        neuralMT: true;
        customGlossary: true;
        domainAdaptation: true;
      };
    };

    // 医学专业引擎
    medical: {
      provider: 'Custom TCM Translation Model';
      features: {
        tcmTerminology: true;
        contextAware: true;
        qualityEstimation: true;
      };
    };
  };

  // 翻译模式
  modes: {
    // 实时翻译
    realTime: {
      enabled: true;
      delay: '<200ms';
      streaming: true;
    };

    // 批量翻译
    batch: {
      enabled: true;
      maxItems: 1000;
    };

    // 文档翻译
    document: {
      enabled: true;
      formats: ['PDF', 'DOCX', 'TXT'];
      preserveFormatting: true;
    };
  };
}
```

### 4.2 医学术语翻译

```typescript
interface MedicalTermTranslation {
  // 术语库
  glossary: {
    // 中医术语
    tcm: {
      syndromes: Map<string, Translations>;
      herbs: Map<string, Translations>;
      acupoints: Map<string, Translations>;
      formulas: Map<string, Translations>;
      techniques: Map<string, Translations>;
    };

    // 西医术语
    western: {
      diseases: Map<string, Translations>;
      procedures: Map<string, Translations>;
      medications: Map<string, Translations>;
      anatomy: Map<string, Translations>;
    };
  };

  // 翻译规则
  rules: {
    // 术语优先
    termPriority: {
      useGlossary: true;
      fallbackToMT: true;
    };

    // 保留原文选项
    preserveOriginal: {
      inParentheses: boolean;    // 翻译 (原文)
      asTooltip: boolean;
    };

    // 拼音/注音
    phonetic: {
      includePinyin: boolean;
      includeBopomofo: boolean;
    };
  };

  // 质量控制
  qualityControl: {
    // 置信度阈值
    confidenceThreshold: number;

    // 人工审核标记
    flagForReview: {
      lowConfidence: boolean;
      newTerms: boolean;
      ambiguous: boolean;
    };
  };
}
```

### 4.3 翻译应用场景

```typescript
interface TranslationUseCases {
  // 1. 病案翻译
  medicalRecordTranslation: {
    // 输入语言 → 输出语言
    sourceToTarget: {
      '中文病案': ['English', 'Malay'],
      '英文报告': ['中文'],
    };

    // 保留医学术语
    preserveTerms: {
      drugNames: true;
      dosages: true;
      measurements: true;
    };
  };

  // 2. 医患沟通翻译
  patientCommunication: {
    // 实时对话翻译
    realTimeDialog: {
      doctorLanguage: string;
      patientLanguage: string;
      bidirectional: true;
    };

    // 简化医学术语
    layman: {
      simplifyTerms: true;
      addExplanations: true;
    };
  };

  // 3. 文献翻译
  literatureTranslation: {
    // 古文翻译
    classicalChinese: {
      toModernChinese: true;
      toEnglish: true;
    };

    // 研究论文
    researchPapers: {
      abstractTranslation: true;
      fullTextTranslation: true;
    };
  };

  // 4. 报告生成
  reportGeneration: {
    // 多语言报告
    multilingualReports: {
      generateInLanguages: string[];
      parallel: boolean;
    };
  };
}
```

### 4.4 翻译界面示例

```
┌─────────────────────────────────────────────────────────────┐
│  AI翻译助手                                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  源语言: [中文] ▼        目标语言: [English] ▼    [🔄 互换]  │
│                                                             │
│  ┌─────────────────────────┬─────────────────────────────┐ │
│  │ 中文输入                │ English Translation        │ │
│  ├─────────────────────────┼─────────────────────────────┤ │
│  │                         │                             │ │
│  │ 患者因"反复头晕1周"就    │ The patient presented with │ │
│  │ 诊。症见头晕目眩，面红    │ "recurrent dizziness for   │ │
│  │ 目赤，急躁易怒，口苦，    │ 1 week". Symptoms include  │ │
│  │ 失眠多梦。               │ dizziness and vertigo,     │ │
│  │                         │ flushed face and red eyes, │ │
│  │ 舌红苔黄，脉弦数。       │ irritability, bitter taste │ │
│  │                         │ in mouth, insomnia with    │ │
│  │ 诊断：眩晕               │ excessive dreaming.        │ │
│  │ 证型：肝阳上亢           │                             │ │
│  │ 治法：平肝潜阳           │ Tongue: red with yellow    │ │
│  │                         │ coating                     │ │
│  │                         │ Pulse: wiry and rapid      │ │
│  │                         │                             │ │
│  │                         │ Diagnosis: Vertigo         │ │
│  │                         │ Syndrome: Liver Yang       │ │
│  │                         │   Rising (肝阳上亢)         │ │
│  │                         │ Treatment: Calm Liver,     │ │
│  │                         │   Subdue Yang              │ │
│  │                         │                             │ │
│  └─────────────────────────┴─────────────────────────────┘ │
│                                                             │
│  📚 术语对照:                                                │
│  • 眩晕 - Vertigo (xuàn yūn)                               │
│  • 肝阳上亢 - Liver Yang Rising (gān yáng shàng kàng)      │
│  • 平肝潜阳 - Calm Liver, Subdue Yang                       │
│                                                             │
│  [🎤 语音输入] [📋 复制翻译] [📄 导出双语报告]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 现代医学治疗方案集成

### 5.1 西医诊断系统

```typescript
interface WesternMedicineDiagnosis {
  // ICD-10编码系统
  icdCoding: {
    version: 'ICD-10-CM';
    search: {
      byKeyword: true;
      byCode: true;
      byCategory: true;
    };
    multilingual: {
      'zh': '中文',
      'en': 'English',
      'ms': 'Malay'
    };
  };

  // 诊断输入
  diagnosisInput: {
    // 主诊断
    primaryDiagnosis: {
      icdCode: string;
      description: string;
      certainty: 'confirmed' | 'suspected' | 'ruled_out';
    };

    // 次要诊断
    secondaryDiagnoses: {
      icdCode: string;
      description: string;
      relationship: 'complication' | 'comorbidity' | 'underlying';
    }[];

    // 与中医诊断关联
    tcmCorrelation: {
      relatedSyndromes: string[];
      integrationNotes: string;
    };
  };

  // 鉴别诊断
  differentialDiagnosis: {
    conditions: {
      name: string;
      icdCode: string;
      likelihood: 'high' | 'medium' | 'low';
      supportingEvidence: string[];
      againstEvidence: string[];
    }[];
  };
}
```

### 5.2 现代医学检查

```typescript
interface ModernMedicalExaminations {
  // 实验室检查
  laboratoryTests: {
    // 常规检查
    routine: {
      bloodRoutine: {          // 血常规
        items: string[];
        referenceRanges: any;
      };
      urineRoutine: {          // 尿常规
        items: string[];
        referenceRanges: any;
      };
      stoolRoutine: {          // 大便常规
        items: string[];
        referenceRanges: any;
      };
    };

    // 生化检查
    biochemistry: {
      liverFunction: string[];  // 肝功能
      renalFunction: string[];  // 肾功能
      bloodLipids: string[];    // 血脂
      bloodGlucose: string[];   // 血糖
      electrolytes: string[];   // 电解质
    };

    // 特殊检查
    special: {
      tumorMarkers: string[];   // 肿瘤标志物
      hormones: string[];       // 激素
      immunology: string[];     // 免疫学
      microbiology: string[];   // 微生物
    };
  };

  // 影像检查
  imaging: {
    xRay: string[];
    ct: string[];
    mri: string[];
    ultrasound: string[];
    endoscopy: string[];
  };

  // 功能检查
  functional: {
    ecg: string[];             // 心电图
    eeg: string[];             // 脑电图
    pulmonaryFunction: string[]; // 肺功能
  };

  // 检查结果录入
  resultEntry: {
    testId: string;
    testDate: Date;
    results: {
      item: string;
      value: string | number;
      unit: string;
      referenceRange: string;
      abnormalFlag: 'high' | 'low' | 'normal' | 'critical';
    }[];
    interpretation: string;
    recommendations: string[];
  };
}
```

### 5.3 西药处方系统

```typescript
interface WesternMedicationSystem {
  // 药物数据库
  drugDatabase: {
    // 药物信息
    drugInfo: {
      genericName: string;
      brandNames: string[];
      atcCode: string;
      drugClass: string;

      // 规格
      formulations: {
        form: string;           // 片剂/胶囊/注射液等
        strength: string;
        packaging: string;
      }[];

      // 适应症
      indications: string[];

      // 用法用量
      dosing: {
        adult: {
          usual: string;
          maximum: string;
          frequency: string;
          route: string;
        };
        pediatric?: any;
        geriatric?: any;
        renalImpairment?: any;
        hepaticImpairment?: any;
      };

      // 禁忌症
      contraindications: string[];

      // 不良反应
      adverseReactions: {
        common: string[];
        uncommon: string[];
        rare: string[];
      };

      // 相互作用
      interactions: {
        drug: string;
        effect: string;
        severity: string;
        management: string;
      }[];
    };
  };

  // 处方开具
  prescription: {
    medications: {
      drug: string;
      dosage: string;
      frequency: string;
      route: string;
      duration: string;
      quantity: number;
      refills?: number;
      instructions: string;
    }[];

    // 处方检查
    safetyChecks: {
      duplicateTherapy: boolean;
      drugInteractions: boolean;
      allergyCheck: boolean;
      dosageCheck: boolean;
      contraindications: boolean;
    };
  };

  // 中西药相互作用
  herbDrugInteractions: {
    herb: string;
    drug: string;
    mechanism: string;
    effect: string;
    severity: 'major' | 'moderate' | 'minor';
    recommendation: string;
    references: string[];
  }[];
}
```

### 5.4 中西医结合治疗方案

```typescript
interface IntegrativeTreatmentPlan {
  // 疾病-证型对照
  diseasesSyndromeCorrelation: {
    // 高血压
    hypertension: {
      icdCode: 'I10';
      commonSyndromes: [
        {
          syndrome: '肝阳上亢',
          characteristics: '头晕头痛，面红目赤，急躁易怒',
          proportion: '30%'
        },
        {
          syndrome: '阴虚阳亢',
          characteristics: '头晕耳鸣，腰膝酸软，五心烦热',
          proportion: '25%'
        },
        {
          syndrome: '痰湿壅盛',
          characteristics: '头重如裹，胸闷脘痞，肢体困重',
          proportion: '20%'
        }
      ];
    };

    // 糖尿病
    diabetes: {
      icdCode: 'E11';
      commonSyndromes: [
        {
          syndrome: '阴虚燥热',
          characteristics: '口渴多饮，多食易饥，尿频量多',
          proportion: '35%'
        },
        {
          syndrome: '气阴两虚',
          characteristics: '神疲乏力，气短懒言，口干',
          proportion: '30%'
        }
      ];
    };
  };

  // 联合治疗方案
  combinedTreatment: {
    condition: string;

    // 西医治疗
    westernTreatment: {
      medications: {
        drug: string;
        purpose: string;
        monitoring: string[];
      }[];
      lifestyle: string[];
      followUp: string;
    };

    // 中医治疗
    tcmTreatment: {
      syndrome: string;
      principle: string;
      formula: {
        name: string;
        modifications: string[];
      };
      acupuncture?: {
        points: string[];
        frequency: string;
      };
    };

    // 协同作用
    synergy: {
      description: string;
      benefits: string[];
      precautions: string[];
    };

    // 监测指标
    monitoring: {
      westernIndicators: string[];
      tcmIndicators: string[];
      frequency: string;
    };
  };

  // 循证医学支持
  evidenceBase: {
    studies: {
      title: string;
      authors: string;
      year: number;
      findings: string;
      evidenceLevel: string;
    }[];

    guidelines: {
      name: string;
      organization: string;
      recommendations: string[];
    }[];
  };
}
```

### 5.5 临床指南数据库

```typescript
interface ClinicalGuidelinesDatabase {
  // 指南来源
  sources: {
    international: [
      'WHO Guidelines',
      'Cochrane Reviews',
      'UpToDate'
    ];

    national: [
      'Malaysia CPG',
      'China TCM Guidelines',
      'Singapore MOH'
    ];

    specialty: [
      'Cardiology Guidelines',
      'Endocrinology Guidelines',
      'TCM Specialty Guidelines'
    ];
  };

  // 指南内容
  guidelineContent: {
    guidelineId: string;
    title: string;
    organization: string;
    version: string;
    publishDate: Date;
    updateDate: Date;

    // 适用疾病
    conditions: string[];

    // 推荐内容
    recommendations: {
      category: string;
      recommendation: string;
      strength: 'strong' | 'weak' | 'conditional';
      evidenceQuality: 'high' | 'moderate' | 'low' | 'very_low';
      references: string[];
    }[];

    // 中医整合建议
    tcmIntegration?: {
      applicableSyndromes: string[];
      recommendations: string[];
      evidence: string[];
    };
  };

  // 智能推荐
  smartRecommendation: {
    // 根据诊断推荐指南
    byDiagnosis: (diagnosis: string) => GuidelineContent[];

    // 根据症状推荐
    bySymptoms: (symptoms: string[]) => GuidelineContent[];

    // 根据治疗需求
    byTreatmentNeed: (need: string) => GuidelineContent[];
  };
}
```

### 5.6 现代医学集成界面

```
┌─────────────────────────────────────────────────────────────┐
│  中西医结合诊疗                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  患者: 张三  性别: 男  年龄: 55岁                              │
│                                                             │
│  ┌─ 诊断 ──────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  西医诊断:                                            │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ 原发性高血压 (I10)                            │     │   │
│  │  │ 2型糖尿病 (E11.9)                             │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  中医诊断:                                            │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ 眩晕 - 肝阳上亢证                              │     │   │
│  │  │ 消渴 - 气阴两虚证                              │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  [添加诊断] [ICD-10查询]                              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 检查结果 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📋 最近检查:                                         │   │
│  │                                                       │   │
│  │  血压: 158/95 mmHg ⚠️                                │   │
│  │  空腹血糖: 8.2 mmol/L ⚠️                              │   │
│  │  HbA1c: 7.8% ⚠️                                      │   │
│  │  血脂: TC 5.8, LDL 3.9 ⚠️                            │   │
│  │                                                       │   │
│  │  [查看趋势] [添加检查]                                │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 联合治疗方案 ─────────────────────────────────────┐   │
│  │                                                       │   │
│  │  💊 西药治疗:                                         │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ 1. Amlodipine 5mg OD - 控制血压              │     │   │
│  │  │ 2. Metformin 500mg BD - 控制血糖             │     │   │
│  │  │ 3. Atorvastatin 20mg ON - 调节血脂          │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  🌿 中药治疗:                                         │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ 天麻钩藤饮合生脉散加减                         │     │   │
│  │  │ 天麻10g 钩藤12g 石决明18g 黄芩9g             │     │   │
│  │  │ 牛膝12g 人参9g 麦冬15g 五味子6g              │     │   │
│  │  │                                             │     │   │
│  │  │ 功效：平肝潜阳，益气养阴                       │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  ⚠️ 中西药相互作用提醒:                               │   │
│  │  • 人参可能增强Metformin降糖作用，需监测血糖          │   │
│  │                                                       │   │
│  │  📍 针灸治疗:                                         │   │
│  │  太冲、风池、曲池、足三里、三阴交                       │   │
│  │  隔日1次，10次为一疗程                                │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 循证医学支持 ─────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📚 相关指南:                                         │   │
│  │  • Malaysia CPG: Management of Hypertension (2018)   │   │
│  │  • 中国高血压中医诊疗指南 (2019)                       │   │
│  │                                                       │   │
│  │  📊 研究支持:                                         │   │
│  │  • 天麻钩藤饮治疗高血压Meta分析显示有效率提高15%        │   │
│  │  • 中西医结合治疗可更好控制血压波动                     │   │
│  │                                                       │   │
│  │  [查看完整指南] [查看研究详情]                          │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 监测计划 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📅 随访计划:                                         │   │
│  │  • 2周后复诊：血压、血糖监测                           │   │
│  │  • 1月后：复查肝肾功能                                │   │
│  │  • 3月后：复查HbA1c、血脂                             │   │
│  │                                                       │   │
│  │  🏠 居家监测:                                         │   │
│  │  • 每日测量血压2次（晨起、睡前）                       │   │
│  │  • 每周测量空腹血糖2次                                │   │
│  │                                                       │   │
│  │  [生成随访提醒] [打印患者指导]                          │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 数据库设计

### 6.1 语音和翻译相关表

```sql
-- 语音识别记录表
CREATE TABLE speech_recognition_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    session_id UUID,

    -- 语音信息
    audio_duration_ms INTEGER,
    audio_format VARCHAR(20),
    audio_sample_rate INTEGER,

    -- 识别结果
    recognized_text TEXT,
    language VARCHAR(10),
    dialect VARCHAR(20),
    confidence DECIMAL(5,2),

    -- 目标字段
    target_entity VARCHAR(50),   -- patient/visit/prescription
    target_field VARCHAR(100),

    -- 后处理
    corrected_text TEXT,
    was_corrected BOOLEAN DEFAULT FALSE,

    -- 元数据
    engine_used VARCHAR(50),
    processing_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 翻译记录表
CREATE TABLE translation_records (
    translation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),

    -- 源文本
    source_text TEXT,
    source_language VARCHAR(10),

    -- 目标文本
    target_text TEXT,
    target_language VARCHAR(10),

    -- 类型
    translation_type VARCHAR(50),  -- medical_record, terminology, communication
    context VARCHAR(100),

    -- 质量
    confidence DECIMAL(5,2),
    reviewed BOOLEAN DEFAULT FALSE,
    reviewer_id UUID,

    -- 元数据
    engine_used VARCHAR(50),
    glossary_terms_used TEXT[],

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 多语言术语表
CREATE TABLE multilingual_terms (
    term_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    term_type VARCHAR(50),         -- syndrome, herb, acupoint, disease

    -- 翻译
    zh_cn VARCHAR(200),
    zh_tw VARCHAR(200),
    en VARCHAR(200),
    ms VARCHAR(200),
    pinyin VARCHAR(200),
    latin VARCHAR(200),

    -- 定义
    definition_zh TEXT,
    definition_en TEXT,

    -- 分类
    category VARCHAR(100),
    subcategory VARCHAR(100),

    -- 元数据
    source VARCHAR(200),
    verified BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户语言偏好表
CREATE TABLE user_language_preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),

    -- 语言设置
    interface_language VARCHAR(10) DEFAULT 'zh-CN',
    input_language VARCHAR(10) DEFAULT 'zh-CN',
    output_language VARCHAR(10) DEFAULT 'zh-CN',
    speech_language VARCHAR(10) DEFAULT 'zh-CN',

    -- 翻译设置
    auto_translate BOOLEAN DEFAULT FALSE,
    show_original BOOLEAN DEFAULT TRUE,
    include_pinyin BOOLEAN DEFAULT FALSE,

    -- 语音设置
    voice_input_enabled BOOLEAN DEFAULT TRUE,
    voice_commands_enabled BOOLEAN DEFAULT TRUE,
    auto_punctuation BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6.2 现代医学相关表

```sql
-- 西医诊断表
CREATE TABLE western_diagnoses (
    diagnosis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id UUID REFERENCES visits(visit_id),

    -- ICD编码
    icd_code VARCHAR(20),
    icd_description TEXT,

    -- 诊断信息
    diagnosis_type VARCHAR(20),   -- primary, secondary
    certainty VARCHAR(20),        -- confirmed, suspected, ruled_out
    onset_date DATE,

    -- 与中医关联
    related_tcm_syndromes TEXT[],
    integration_notes TEXT,

    -- 元数据
    diagnosed_by UUID REFERENCES practitioners(practitioner_id),
    diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 西药处方表
CREATE TABLE western_prescriptions (
    prescription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    visit_id UUID REFERENCES visits(visit_id),

    -- 处方信息
    prescription_date TIMESTAMP,
    status VARCHAR(20),

    -- 药物列表
    medications JSONB,  -- [{drug, dosage, frequency, route, duration, quantity}]

    -- 安全检查结果
    safety_checks JSONB,

    -- 处方者
    prescriber_id UUID REFERENCES practitioners(practitioner_id),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 检查结果表
CREATE TABLE examination_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(patient_id),
    visit_id UUID REFERENCES visits(visit_id),

    -- 检查信息
    test_type VARCHAR(100),       -- lab, imaging, functional
    test_name VARCHAR(200),
    test_date DATE,

    -- 结果
    results JSONB,                -- [{item, value, unit, reference, flag}]
    interpretation TEXT,
    recommendations TEXT[],

    -- 文件
    report_file_url TEXT,

    -- 元数据
    ordered_by UUID,
    performed_by VARCHAR(200),
    facility VARCHAR(200),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 临床指南表
CREATE TABLE clinical_guidelines (
    guideline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 基本信息
    title VARCHAR(500),
    organization VARCHAR(200),
    version VARCHAR(50),
    publish_date DATE,
    update_date DATE,

    -- 内容
    applicable_conditions TEXT[],
    recommendations JSONB,
    tcm_integration JSONB,

    -- 文件
    document_url TEXT,

    -- 状态
    is_current BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 中西药相互作用表
CREATE TABLE herb_drug_interactions (
    interaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 药物信息
    herb_name VARCHAR(100),
    drug_name VARCHAR(100),
    drug_class VARCHAR(100),

    -- 相互作用
    mechanism TEXT,
    clinical_effect TEXT,
    severity VARCHAR(20),        -- major, moderate, minor
    documentation VARCHAR(20),   -- established, probable, suspected

    -- 管理建议
    management TEXT,
    monitoring TEXT[],

    -- 参考文献
    references TEXT[],

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_speech_records_user ON speech_recognition_records(user_id);
CREATE INDEX idx_translation_user ON translation_records(user_id);
CREATE INDEX idx_terms_type ON multilingual_terms(term_type);
CREATE INDEX idx_western_diag_visit ON western_diagnoses(visit_id);
CREATE INDEX idx_exam_results_patient ON examination_results(patient_id);
CREATE INDEX idx_herb_drug_herb ON herb_drug_interactions(herb_name);
CREATE INDEX idx_herb_drug_drug ON herb_drug_interactions(drug_name);
```

---

## 7. API接口设计

### 7.1 语音识别API

```typescript
// 语音识别API
interface SpeechRecognitionAPI {
  // 开始实时识别
  POST '/api/speech/start-streaming': {
    request: {
      language: string;
      dialect?: string;
      medicalEnhancement: boolean;
      targetField?: string;
    };
    response: {
      sessionId: string;
      websocketUrl: string;
    };
  };

  // WebSocket消息
  WebSocket '/ws/speech/{sessionId}': {
    // 发送音频数据
    send: {
      type: 'audio';
      data: ArrayBuffer;
    };

    // 接收识别结果
    receive: {
      type: 'partial' | 'final';
      text: string;
      confidence: number;
      alternatives?: string[];
    };
  };

  // 批量识别
  POST '/api/speech/recognize': {
    request: {
      audio: File;
      language: string;
      format: string;
    };
    response: {
      text: string;
      confidence: number;
      segments: {
        text: string;
        startTime: number;
        endTime: number;
      }[];
    };
  };
}
```

### 7.2 翻译API

```typescript
// 翻译API
interface TranslationAPI {
  // 文本翻译
  POST '/api/translate/text': {
    request: {
      text: string;
      sourceLanguage: string;
      targetLanguage: string;
      context?: 'medical' | 'general';
      preserveTerms?: boolean;
    };
    response: {
      translatedText: string;
      confidence: number;
      terms: {
        original: string;
        translated: string;
        pinyin?: string;
      }[];
    };
  };

  // 批量翻译
  POST '/api/translate/batch': {
    request: {
      items: {
        id: string;
        text: string;
      }[];
      sourceLanguage: string;
      targetLanguage: string;
    };
    response: {
      translations: {
        id: string;
        text: string;
        translatedText: string;
      }[];
    };
  };

  // 术语查询
  GET '/api/translate/term/{term}': {
    response: {
      term: string;
      translations: {
        [language: string]: string;
      };
      pinyin?: string;
      definition?: string;
    };
  };

  // 语言检测
  POST '/api/translate/detect': {
    request: {
      text: string;
    };
    response: {
      language: string;
      confidence: number;
      alternatives: {
        language: string;
        confidence: number;
      }[];
    };
  };
}
```

### 7.3 现代医学API

```typescript
// 现代医学API
interface ModernMedicineAPI {
  // ICD-10查询
  GET '/api/icd10/search': {
    query: {
      q: string;
      language?: string;
      limit?: number;
    };
    response: {
      results: {
        code: string;
        description: string;
        category: string;
      }[];
    };
  };

  // 获取药物信息
  GET '/api/drugs/{drugId}': {
    response: {
      drugInfo: DrugInfo;
      interactions: DrugInteraction[];
      herbInteractions: HerbDrugInteraction[];
    };
  };

  // 药物相互作用检查
  POST '/api/drugs/interaction-check': {
    request: {
      drugs: string[];
      herbs?: string[];
    };
    response: {
      drugDrugInteractions: Interaction[];
      herbDrugInteractions: Interaction[];
      warnings: Warning[];
    };
  };

  // 获取临床指南
  GET '/api/guidelines/search': {
    query: {
      condition?: string;
      keyword?: string;
    };
    response: {
      guidelines: Guideline[];
    };
  };

  // 检查结果录入
  POST '/api/examinations/results': {
    request: {
      patientId: string;
      visitId: string;
      testType: string;
      testName: string;
      results: TestResult[];
    };
    response: {
      resultId: string;
      abnormalFlags: string[];
      suggestions: string[];
    };
  };

  // 中西医关联建议
  POST '/api/integrative/suggestions': {
    request: {
      westernDiagnosis: string;
      tcmSyndrome?: string;
    };
    response: {
      correlations: DiseaseCorrelation[];
      combinedTreatments: CombinedTreatment[];
      evidence: Evidence[];
    };
  };
}
```

---

## 8. 界面设计

### 8.1 语音输入界面组件

```
┌─────────────────────────────────────────────────────────────┐
│  主诉症状                                          🎤 语音输入 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │  头晕目眩3天，伴头痛、面红目赤                         │   │
│  │  █                                                  │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 语音控制 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🔴 正在录音...  [■ 停止]                             │   │
│  │                                                       │   │
│  │  语言: [普通话] ▼  方言: [无] ▼                        │   │
│  │                                                       │   │
│  │  💡 语音命令：说"句号"添加标点，说"下一项"跳转           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 多语言报告界面

```
┌─────────────────────────────────────────────────────────────┐
│  病案报告 - 多语言版本                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  语言: [中文] [English] [Bahasa Melayu]    [📄 导出全部]     │
│                                                             │
│  ┌─ 中文 ─────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  诊断：眩晕                                           │   │
│  │  证型：肝阳上亢证                                      │   │
│  │  治法：平肝潜阳，清热熄风                               │   │
│  │                                                       │   │
│  │  处方：天麻钩藤饮加减                                   │   │
│  │  天麻10g 钩藤12g 石决明18g...                         │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ English ─────────────────────────────────────────┐     │
│  │                                                       │   │
│  │  Diagnosis: Vertigo                                   │   │
│  │  Syndrome: Liver Yang Rising                          │   │
│  │            (肝阳上亢证, Gān Yáng Shàng Kàng)           │   │
│  │  Treatment: Calm Liver, Subdue Yang,                  │   │
│  │            Clear Heat, Extinguish Wind                │   │
│  │                                                       │   │
│  │  Formula: Tian Ma Gou Teng Yin Modified               │   │
│  │  Gastrodia 10g, Uncaria 12g, Haliotis 18g...         │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  [🖨️ 打印] [📧 发送邮件] [📱 发送至患者App]                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. 技术选型

### 9.1 语音识别技术

| 功能 | 推荐技术 | 备选 |
|------|----------|------|
| 云端ASR | Azure Speech Service | Google Cloud Speech-to-Text |
| 离线ASR | Vosk | Mozilla DeepSpeech |
| 中医术语模型 | 自定义语言模型 | Fine-tuned Whisper |
| 方言识别 | 科大讯飞 | Azure Custom Speech |

### 9.2 翻译技术

| 功能 | 推荐技术 | 备选 |
|------|----------|------|
| 神经机器翻译 | DeepL API | Google Cloud Translation |
| 医学术语翻译 | 自定义术语库 + NMT | Custom Transformer Model |
| 语言检测 | FastText | langdetect |

### 9.3 现代医学数据

| 数据 | 来源 |
|------|------|
| ICD-10编码 | WHO ICD-10 Database |
| 药物数据 | DrugBank, Malaysia NPCB |
| 临床指南 | PubMed, Malaysia CPG |
| 中西药相互作用 | Natural Medicines Database |

---

## 10. 实施计划

### 10.1 阶段规划

```
阶段1: 语音识别基础（第1-2月）
├── ASR引擎集成
├── 实时语音识别
├── 基础语音命令
└── 中医术语自定义词汇

阶段2: 多语言支持（第3-4月）
├── 界面多语言
├── 术语多语言数据库
├── 方言识别支持
└── 语言切换机制

阶段3: AI翻译系统（第5-6月）
├── 翻译引擎集成
├── 医学术语库
├── 实时翻译功能
└── 翻译质量优化

阶段4: 现代医学集成（第7-9月）
├── ICD-10编码系统
├── 西药数据库
├── 检查结果管理
├── 中西医关联
└── 临床指南数据库

阶段5: 优化和测试（第10-11月）
├── 性能优化
├── 准确率提升
├── 用户测试
└── 修复完善
```

### 10.2 预算估算

| 类别 | 项目 | 预算 (RM) |
|------|------|-----------|
| **语音识别** | ASR引擎授权（年）| 60,000 |
| | 自定义模型开发 | 80,000 |
| | 方言支持开发 | 50,000 |
| **翻译** | 翻译API（年）| 40,000 |
| | 术语库建设 | 60,000 |
| | 翻译模型优化 | 50,000 |
| **现代医学** | 数据库授权 | 30,000 |
| | 指南集成 | 40,000 |
| | 相互作用数据 | 30,000 |
| **开发** | 后端开发 | 150,000 |
| | 前端开发 | 100,000 |
| | 测试和QA | 50,000 |
| **总计** | | **740,000** |

### 10.3 关键成功因素

1. **语音识别准确率** - 中医术语识别准确率需达到95%以上
2. **翻译质量** - 医学术语翻译需准确一致
3. **响应速度** - 实时识别延迟<500ms
4. **用户体验** - 简单直观的操作界面
5. **数据质量** - 高质量的多语言术语库和现代医学数据

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0 | 2025-11-17 | 初始版本 |

---

**文档结束**
