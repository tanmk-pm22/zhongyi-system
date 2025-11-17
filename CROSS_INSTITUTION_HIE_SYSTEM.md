# 跨机构病案共享与AI智能整合系统

## 版本: 1.0
## 日期: 2025年11月17日

---

## 目录

1. [系统概述](#1-系统概述)
2. [马来西亚HIE法规要求](#2-马来西亚hie法规要求)
3. [跨机构数据共享架构](#3-跨机构数据共享架构)
4. [病案索取流程](#4-病案索取流程)
5. [AI智能整合分析](#5-ai智能整合分析)
6. [数据标准和互操作性](#6-数据标准和互操作性)
7. [隐私和安全](#7-隐私和安全)
8. [数据库设计](#8-数据库设计)
9. [界面设计](#9-界面设计)
10. [实施建议](#10-实施建议)

---

## 1. 系统概述

### 1.1 功能目标

构建一个跨医院和诊所的病案共享系统，让中医师能够：

1. **索取外部病案** - 获取患者在其他医疗机构的诊疗记录
2. **整合治疗历史** - 汇总中医和西医的所有治疗记录
3. **AI智能分析** - 自动提取关键信息，补全病案
4. **全面了解病情** - 提供完整的患者健康画像

### 1.2 核心价值

```
┌─────────────────────────────────────────────────────────────┐
│                 跨机构病案共享系统价值                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  对医生                          对患者                      │
│  ────────                        ────────                   │
│  • 完整了解病史                   • 避免重复检查               │
│  • 避免重复用药                   • 减少医疗费用               │
│  • 更准确的诊断                   • 提高治疗效果               │
│  • 减少医疗风险                   • 连续性医疗服务             │
│                                                             │
│  对中医诊疗                       对医疗系统                  │
│  ────────────                    ────────────               │
│  • 了解西医治疗背景               • 减少医疗资源浪费            │
│  • 中西医配合治疗                 • 提高医疗效率               │
│  • 避免中西药冲突                 • 促进医疗协作               │
│  • 更好的辨证依据                 • 数据驱动的医疗决策          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 马来西亚HIE法规要求

### 2.1 法律框架

```typescript
interface MalaysiaHIERegulations {
  // 个人数据保护法
  PDPA2010: {
    // 敏感个人数据
    sensitiveData: {
      includes: ['health_records', 'medical_history'];
      requirements: {
        explicitConsent: true;       // 明确同意
        purpose: 'specified';        // 指定目的
        disclosure: 'authorized';    // 授权披露
      };
    };

    // 数据主体权利
    dataSubjectRights: {
      access: true;                  // 访问权
      correction: true;              // 更正权
      withdrawal: true;              // 撤回同意权
    };

    // 跨境传输
    crossBorder: {
      allowed: 'with_equivalent_protection';
      requirements: ['ministerial_approval', 'consent'];
    };
  };

  // 医疗法规
  medicalRegulations: {
    // 医疗记录保存
    recordRetention: {
      adults: '7_years';
      minors: '7_years_after_21';
      newborns: '25_years';
    };

    // 医疗信息披露
    disclosure: {
      requiresConsent: true;
      exceptions: [
        'court_order',
        'public_health_emergency',
        'patient_incapacity'
      ];
    };
  };

  // MOH指南
  mohGuidelines: {
    // 医疗信息系统
    healthIT: {
      interoperability: 'required';
      standards: ['HL7', 'FHIR'];
      security: 'ISO27001';
    };

    // 电子同意
    eConsent: {
      allowed: true;
      requirements: [
        'audit_trail',
        'identity_verification',
        'withdrawal_mechanism'
      ];
    };
  };
}
```

### 2.2 合规要求清单

| 要求 | 描述 | 实施方式 |
|------|------|----------|
| 患者同意 | 获取明确书面同意 | 电子同意书 + 签名 |
| 目的限制 | 只用于医疗目的 | 访问控制 + 审计 |
| 最小必要 | 只索取必要信息 | 数据过滤机制 |
| 安全传输 | 加密传输数据 | TLS 1.3 + E2E加密 |
| 访问记录 | 记录所有访问 | 完整审计日志 |
| 数据更正 | 支持患者更正 | 更正请求流程 |
| 撤回同意 | 支持撤回同意 | 同意管理系统 |

---

## 3. 跨机构数据共享架构

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                   跨机构病案共享架构                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                      ┌─────────────┐      │
│  │ 您的诊所     │                      │ 外部医院A    │      │
│  │ TCM Clinic  │◄─────────────────────►│ Hospital A  │      │
│  └──────┬──────┘                      └─────────────┘      │
│         │                                                   │
│         │              ┌─────────────┐                      │
│         │              │ HIE中枢平台  │                      │
│         ├─────────────►│             │◄─────────────┐       │
│         │              │ • 身份认证   │              │       │
│         │              │ • 同意管理   │              │       │
│         │              │ • 数据路由   │      ┌───────┴─────┐ │
│         │              │ • 审计日志   │      │ 外部诊所B    │ │
│         │              └──────┬──────┘      │ Clinic B   │ │
│         │                     │             └─────────────┘ │
│         │                     │                             │
│         │              ┌──────┴──────┐                      │
│         │              │ 马来西亚医疗  │                      │
│         └─────────────►│ 信息网络     │                      │
│                        │ MyHIX/NHIS  │                      │
│                        └─────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 数据共享模式

```typescript
interface DataSharingModels {
  // 模式1: 集中式（通过国家平台）
  centralizedModel: {
    description: '通过马来西亚国家医疗信息系统';
    platform: 'MyHIX (Malaysia Health Information Exchange)';

    advantages: [
      '标准化数据格式',
      '统一身份认证',
      '国家级安全保障'
    ];

    limitations: [
      '覆盖范围有限',
      '主要是公立医院',
      '私人诊所参与少'
    ];

    implementation: {
      register: '向MOH注册为HIE参与者';
      certification: '获得系统认证';
      integration: '集成MyHIX API';
    };
  };

  // 模式2: 点对点（直接交换）
  peerToPeerModel: {
    description: '与合作机构直接建立数据交换';

    advantages: [
      '灵活性高',
      '快速部署',
      '可定制化'
    ];

    limitations: [
      '需逐一建立连接',
      '标准化挑战',
      '管理复杂'
    ];

    implementation: {
      agreement: '签订数据共享协议';
      technical: 'API对接或FHIR交换';
      security: 'VPN或加密通道';
    };
  };

  // 模式3: 患者主导（PHR）
  patientMediatedModel: {
    description: '患者自己获取并提供病案';

    advantages: [
      '无需机构间协议',
      '患者完全控制',
      '简单直接'
    ];

    limitations: [
      '数据完整性难保证',
      '格式不统一',
      '患者负担重'
    ];

    implementation: {
      upload: '患者上传病案文件';
      ocr: 'AI提取文本信息';
      verification: '可选的来源验证';
    };
  };

  // 模式4: 混合模式（推荐）
  hybridModel: {
    description: '结合以上多种模式';

    components: {
      national: 'MyHIX集成（公立医院）';
      bilateral: '与主要私立医院直连';
      patientUpload: '支持患者自行上传';
    };

    advantages: [
      '最大覆盖范围',
      '灵活适应性强',
      '渐进式扩展'
    ];
  };
}
```

### 3.3 数据交换标准

```typescript
interface DataExchangeStandards {
  // HL7 FHIR R4
  fhir: {
    version: 'R4';

    // 支持的资源类型
    resources: {
      patient: 'Patient';
      encounter: 'Encounter';
      condition: 'Condition';
      medicationRequest: 'MedicationRequest';
      procedure: 'Procedure';
      observation: 'Observation';
      diagnosticReport: 'DiagnosticReport';
      allergyIntolerance: 'AllergyIntolerance';
      immunization: 'Immunization';
    };

    // 中医扩展
    tcmExtensions: {
      tcmDiagnosis: 'Extension for TCM syndrome';
      tcmPrescription: 'Extension for herbal formula';
      acupunctureTreatment: 'Extension for acupuncture';
    };
  };

  // ICD编码
  coding: {
    diseases: 'ICD-10-CM';
    procedures: 'ICD-10-PCS';
    medications: 'ATC';
    tcmDiseases: 'GB/T 15657';  // 中医疾病分类
    tcmSyndromes: 'GB/T 16751'; // 中医证候分类
  };
}
```

---

## 4. 病案索取流程

### 4.1 完整流程

```
┌─────────────────────────────────────────────────────────────┐
│                    病案索取完整流程                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 患者同意                                                 │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 患者登记 │ → │ 解释目的 │ → │ 签署同意 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       ↓                                                     │
│  2. 发起请求                                                 │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 选择机构 │ → │ 选择数据 │ → │ 提交请求 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       ↓                                                     │
│  3. 身份验证                                                 │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 医生认证 │ → │ 患者验证 │ → │ 授权确认 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       ↓                                                     │
│  4. 数据传输                                                 │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 加密传输 │ → │ 数据接收 │ → │ 格式转换 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       ↓                                                     │
│  5. AI处理                                                   │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 数据解析 │ → │ 信息提取 │ → │ 智能整合 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│       ↓                                                     │
│  6. 呈现结果                                                 │
│  ────────────                                               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ 统一视图 │ → │ AI分析   │ → │ 医生审阅 │                 │
│  └─────────┘    └─────────┘    └─────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 同意管理系统

```typescript
interface ConsentManagement {
  // 同意书模板
  consentForm: {
    // 基本信息
    patientInfo: {
      name: string;
      nric: string;
      dateOfBirth: string;
    };

    // 同意内容
    consentScope: {
      // 数据类型
      dataTypes: {
        demographics: boolean;
        medicalHistory: boolean;
        diagnoses: boolean;
        medications: boolean;
        labResults: boolean;
        imaging: boolean;
        procedures: boolean;
        allergies: boolean;
      };

      // 时间范围
      timeRange: {
        from: Date | 'all_history';
        to: Date | 'current';
      };

      // 来源机构
      sourceInstitutions: {
        all: boolean;
        specific: string[];
      };

      // 有效期
      validity: {
        duration: '6_months' | '1_year' | '2_years' | 'until_revoked';
        startDate: Date;
        endDate?: Date;
      };
    };

    // 目的说明
    purposeStatement: string;

    // 患者权利
    patientRights: {
      accessRight: string;
      correctionRight: string;
      withdrawalRight: string;
      complaintRight: string;
    };

    // 签名
    signature: {
      patientSignature: string;       // 数字签名或图像
      signedAt: Date;
      witnessSignature?: string;
      witnessName?: string;
    };
  };

  // 同意状态管理
  consentStatus: {
    active: boolean;
    createdAt: Date;
    lastUsedAt: Date;
    timesUsed: number;
    revokedAt?: Date;
    revokedReason?: string;
  };

  // 同意验证
  consentVerification: {
    // 验证请求是否符合同意范围
    validateRequest: (request: DataRequest) => {
      valid: boolean;
      reason?: string;
    };

    // 记录使用
    logUsage: (requestId: string) => void;
  };
}
```

### 4.3 数据请求接口

```typescript
interface ExternalDataRequest {
  // 请求信息
  requestInfo: {
    requestId: string;
    requestingPractitioner: {
      id: string;
      name: string;
      license: string;
      institution: string;
    };
    requestDate: Date;
    urgency: 'routine' | 'urgent' | 'emergency';
  };

  // 患者信息
  patient: {
    identifier: {
      type: 'NRIC' | 'Passport' | 'MyKad';
      value: string;
    };
    name: string;
    dateOfBirth: Date;
  };

  // 请求内容
  requestedData: {
    // 数据类别
    categories: (
      | 'encounters'           // 就诊记录
      | 'diagnoses'           // 诊断
      | 'medications'         // 用药
      | 'procedures'          // 手术/治疗
      | 'lab_results'         // 检验结果
      | 'imaging'             // 影像
      | 'vital_signs'         // 生命体征
      | 'allergies'           // 过敏
      | 'immunizations'       // 免疫接种
      | 'tcm_treatments'      // 中医治疗
    )[];

    // 时间范围
    dateRange: {
      from: Date;
      to: Date;
    };

    // 来源机构（可选）
    sourceInstitutions?: string[];

    // 特定条件筛选
    filters?: {
      diagnosisCodes?: string[];
      medicationCodes?: string[];
      departmentTypes?: string[];
    };
  };

  // 同意引用
  consentReference: {
    consentId: string;
    verificationCode: string;
  };
}

// 响应
interface ExternalDataResponse {
  responseInfo: {
    requestId: string;
    responseDate: Date;
    status: 'complete' | 'partial' | 'no_data' | 'error';
    sources: {
      institution: string;
      recordsReturned: number;
    }[];
  };

  // 返回的数据（FHIR格式）
  data: {
    bundle: any;  // FHIR Bundle
  };

  // 元数据
  metadata: {
    totalRecords: number;
    dataCompleteness: number;  // 0-100%
    warnings?: string[];
  };
}
```

---

## 5. AI智能整合分析

### 5.1 外部数据AI处理流程

```typescript
interface AIDataIntegration {
  // 步骤1: 数据标准化
  dataStandardization: {
    // 格式转换
    formatConversion: {
      input: ['FHIR', 'HL7v2', 'CDA', 'PDF', 'Image'];
      output: 'unified_internal_format';
    };

    // 术语映射
    terminologyMapping: {
      // ICD-10 → 中医疾病
      diagnosisMapping: (icdCode: string) => {
        tcmDisease: string;
        tcmCategory: string;
        relatedSyndromes: string[];
      };

      // 西药 → 中药交互
      medicationMapping: (atcCode: string) => {
        drugName: string;
        tcmInteractions: string[];
        cautions: string[];
      };
    };

    // 时间线对齐
    timelineAlignment: {
      mergeOverlapping: boolean;
      sortChronologically: boolean;
      detectGaps: boolean;
    };
  };

  // 步骤2: 信息提取
  informationExtraction: {
    // 结构化数据提取
    structuredExtraction: {
      diagnoses: string[];
      medications: any[];
      procedures: any[];
      labResults: any[];
    };

    // 非结构化文本处理
    unstructuredProcessing: {
      // OCR处理（扫描文件）
      ocr: {
        languages: ['zh', 'en', 'ms'];
        accuracy: number;
      };

      // NLP提取
      nlp: {
        entityRecognition: [
          'symptoms',
          'diagnoses',
          'medications',
          'dosages',
          'frequencies',
          'durations'
        ];
        relationExtraction: boolean;
        negationDetection: boolean;
      };
    };
  };

  // 步骤3: 智能分析
  intelligentAnalysis: {
    // 治疗历史分析
    treatmentHistoryAnalysis: {
      // 用药模式
      medicationPattern: {
        currentMedications: any[];
        pastMedications: any[];
        adherenceIndicators: string[];
        effectivenessIndicators: string[];
      };

      // 治疗效果评估
      treatmentEffectiveness: {
        conditions: {
          condition: string;
          treatments: string[];
          outcomes: string[];
          responseLevel: 'good' | 'moderate' | 'poor' | 'unknown';
        }[];
      };

      // 复发模式
      recurrencePattern: {
        conditions: string[];
        frequency: string;
        triggers: string[];
      };
    };

    // 风险识别
    riskIdentification: {
      // 药物风险
      medicationRisks: {
        drugInteractions: any[];
        duplicateTherapy: any[];
        contraindicatedDrugs: any[];
        herbDrugInteractions: any[];
      };

      // 疾病风险
      diseaseRisks: {
        chronicConditions: string[];
        complications: string[];
        progressionIndicators: string[];
      };

      // 治疗缺口
      treatmentGaps: {
        missingFollowups: string[];
        discontinuedTreatments: string[];
        unaddressedConditions: string[];
      };
    };

    // 中医辨证提示
    tcmSyndromeHints: {
      // 从西医数据推断中医证候
      inferredPatterns: {
        // 从症状群推断
        fromSymptoms: string[];
        // 从检查结果推断
        fromLabResults: string[];
        // 从用药史推断
        fromMedications: string[];
      };

      // 建议的问诊方向
      suggestedInquiry: string[];

      // 需要关注的证候
      syndromeAlerts: string[];
    };
  };

  // 步骤4: 生成整合报告
  integratedReport: {
    // 患者健康概览
    healthOverview: {
      summary: string;
      keyConditions: string[];
      currentStatus: string;
    };

    // 治疗时间线
    treatmentTimeline: {
      events: {
        date: Date;
        type: string;
        institution: string;
        description: string;
        outcome?: string;
      }[];
    };

    // 当前用药清单
    currentMedications: {
      medication: string;
      indication: string;
      prescribedBy: string;
      startDate: Date;
      tcmConsiderations: string[];
    }[];

    // 重要发现
    keyFindings: {
      finding: string;
      source: string;
      relevance: string;
      action: string;
    }[];

    // AI建议
    aiRecommendations: {
      diagnosticConsiderations: string[];
      treatmentConsiderations: string[];
      precautions: string[];
      suggestedFollowups: string[];
    };
  };
}
```

### 5.2 AI补全功能

```typescript
interface AIAutoComplete {
  // 病史补全
  medicalHistoryCompletion: {
    input: {
      externalRecords: any[];
      currentAssessment: any;
    };

    output: {
      // 自动填充的既往史
      pastMedicalHistory: {
        confirmed: {          // 确认的信息
          conditions: string[];
          surgeries: string[];
          hospitalizations: string[];
        };
        inferred: {           // 推断的信息（需医生确认）
          possibleConditions: string[];
          suggestedInquiries: string[];
        };
      };

      // 自动填充的用药史
      medicationHistory: {
        current: any[];
        past: any[];
        allergies: string[];
        adverseReactions: string[];
      };

      // 自动填充的家族史线索
      familyHistoryHints: string[];
    };
  };

  // 检查结果整合
  labResultIntegration: {
    // 按类别整理
    categorizedResults: {
      bloodTests: any[];
      urineTests: any[];
      imaging: any[];
      other: any[];
    };

    // 趋势分析
    trendAnalysis: {
      parameter: string;
      values: { date: Date; value: number }[];
      trend: 'improving' | 'stable' | 'worsening';
      normalRange: { min: number; max: number };
    }[];

    // 异常标记
    abnormalFlags: {
      parameter: string;
      value: string;
      severity: 'mild' | 'moderate' | 'severe';
      clinicalSignificance: string;
      tcmImplication: string;
    }[];
  };

  // 治疗建议补全
  treatmentSuggestionCompletion: {
    // 基于外部治疗史
    basedOnHistory: {
      // 有效的治疗
      effectiveTreatments: {
        treatment: string;
        evidence: string;
        suggestion: string;
      }[];

      // 无效的治疗
      ineffectiveTreatments: {
        treatment: string;
        evidence: string;
        avoidReason: string;
      }[];

      // 可考虑的替代方案
      alternatives: string[];
    };

    // 中西医结合建议
    integrativeSuggestions: {
      currentWesternTreatment: string;
      tcmComplementary: string[];
      precautions: string[];
      monitoringPoints: string[];
    }[];
  };
}
```

### 5.3 AI分析界面

```
┌─────────────────────────────────────────────────────────────┐
│  外部病案AI整合分析                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  患者: 张三  NRIC: xxxxxx-xx-xxxx                            │
│  数据来源: 中央医院(15条) | 仁爱诊所(8条) | 患者上传(3份)        │
│                                                             │
│  ┌─ AI健康概览 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📊 主要健康问题:                                      │   │
│  │  • 2型糖尿病（确诊5年，口服药物控制中）                   │   │
│  │  • 高血压（确诊3年，服用ARB类药物）                      │   │
│  │  • 慢性胃炎（反复发作）                                 │   │
│  │                                                       │   │
│  │  💊 当前西药:                                          │   │
│  │  • Metformin 500mg BD                                 │   │
│  │  • Losartan 50mg OD                                   │   │
│  │  • Omeprazole 20mg OD                                 │   │
│  │                                                       │   │
│  │  ⚠️ AI提示:                                           │   │
│  │  • Metformin长期使用可能导致气阴两虚                     │   │
│  │  • 建议关注脾胃功能                                    │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 治疗时间线 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  2025-11 ──●── 本次就诊（您的诊所）                     │   │
│  │            │                                          │   │
│  │  2025-10 ──●── 糖尿病复诊（中央医院）                   │   │
│  │            │   HbA1c: 7.2%（较前略升）                  │   │
│  │            │                                          │   │
│  │  2025-08 ──●── 胃痛发作（仁爱诊所）                     │   │
│  │            │   诊断：急性胃炎，予PPI治疗                 │   │
│  │            │                                          │   │
│  │  2025-06 ──●── 血压偏高（中央医院）                     │   │
│  │            │   BP: 145/92，调整药物剂量                 │   │
│  │            │                                          │   │
│  │  [展开完整时间线]                                      │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ AI中医辨证提示 ────────────────────────────────────┐   │
│  │                                                       │   │
│  │  🔍 从外部病案推断的中医线索:                            │   │
│  │                                                       │   │
│  │  1. 糖尿病+高血压病史 → 可能存在:                       │   │
│  │     • 肝肾阴虚                                        │   │
│  │     • 瘀血阻络                                        │   │
│  │     💡 建议问诊：口干、腰膝酸软、视物模糊               │   │
│  │                                                       │   │
│  │  2. 反复胃炎 + 长期用药 → 可能存在:                     │   │
│  │     • 脾胃虚弱                                        │   │
│  │     • 肝胃不和                                        │   │
│  │     💡 建议问诊：食欲、大便、情志                       │   │
│  │                                                       │   │
│  │  3. 检验指标提示:                                      │   │
│  │     • HbA1c上升 → 阴虚内热可能加重                      │   │
│  │     • 空腹血糖波动 → 气阴两虚                          │   │
│  │                                                       │   │
│  │  [采纳建议] [查看详细分析]                              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 检验结果趋势 ───────────────────────────────────────┐   │
│  │                                                       │   │
│  │  HbA1c (%)                         血压 (mmHg)        │   │
│  │  8 ┤                               150 ┤    ╭─        │   │
│  │    │    ╭──╮                           │   ╱          │   │
│  │  7 ┤   ╱    ╲   ╭─                 140 ┤  ╱           │   │
│  │    │  ╱      ╲ ╱                       │ ╱ 收缩压     │   │
│  │  6 ┤ ╱        ╲                    130 ┼╱             │   │
│  │    ├─────────────                      ├─────────     │   │
│  │    2024  2025                          2024  2025     │   │
│  │                                                       │   │
│  │  ⚠️ HbA1c近期上升趋势，建议加强血糖控制                 │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ AI治疗建议 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📋 中西医结合建议:                                    │   │
│  │                                                       │   │
│  │  1. 糖尿病管理:                                       │   │
│  │     西医：继续Metformin，监测HbA1c                     │   │
│  │     中医：配合滋阴降火、益气养阴法                       │   │
│  │     推荐：六味地黄丸加减                                │   │
│  │     ⚠️ 注意：避免用甘草（影响血压）                     │   │
│  │                                                       │   │
│  │  2. 高血压管理:                                       │   │
│  │     西医：继续Losartan                                │   │
│  │     中医：配合平肝潜阳法                                │   │
│  │     推荐：天麻钩藤饮加减                                │   │
│  │                                                       │   │
│  │  3. 胃病调理:                                         │   │
│  │     考虑脾胃虚弱证，可用香砂六君子汤                     │   │
│  │     💡 若有肝胃不和症状，配合疏肝和胃                    │   │
│  │                                                       │   │
│  │  [生成处方建议] [导入病案]                              │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 注意事项和禁忌 ────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ⚠️ 药物相互作用提醒:                                  │   │
│  │                                                       │   │
│  │  • 甘草 + Losartan → 可能加重高血压，建议避免           │   │
│  │  • 黄芪 + Metformin → 可能增强降糖作用，需监测血糖      │   │
│  │  • 丹参 + 抗血小板药 → 增加出血风险                     │   │
│  │                                                       │   │
│  │  [查看完整相互作用列表]                                 │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 数据标准和互操作性

### 6.1 FHIR资源映射

```typescript
// 中医FHIR扩展定义
interface TCMFHIRExtensions {
  // 中医诊断扩展
  tcmCondition: {
    resourceType: 'Condition';
    extension: [
      {
        url: 'http://tcm.org/fhir/StructureDefinition/tcm-syndrome';
        valueCodeableConcept: {
          coding: [{
            system: 'http://tcm.org/fhir/CodeSystem/tcm-syndromes';
            code: string;      // 证型代码
            display: string;   // 证型名称
          }];
        };
      },
      {
        url: 'http://tcm.org/fhir/StructureDefinition/tcm-etiology';
        valueString: string;   // 病因
      },
      {
        url: 'http://tcm.org/fhir/StructureDefinition/tcm-pathogenesis';
        valueString: string;   // 病机
      }
    ];
  };

  // 中药处方扩展
  tcmMedicationRequest: {
    resourceType: 'MedicationRequest';
    extension: [
      {
        url: 'http://tcm.org/fhir/StructureDefinition/tcm-formula';
        valueReference: {
          reference: string;   // 方剂引用
        };
      },
      {
        url: 'http://tcm.org/fhir/StructureDefinition/tcm-preparation';
        valueCodeableConcept: {
          coding: [{
            system: 'http://tcm.org/fhir/CodeSystem/preparation-methods';
            code: string;      // 煎服法
          }];
        };
      }
    ];
  };

  // 针灸治疗扩展
  acupunctureProcedure: {
    resourceType: 'Procedure';
    extension: [
      {
        url: 'http://tcm.org/fhir/StructureDefinition/acupoints-used';
        valueCodeableConcept: {
          coding: [{
            system: 'http://tcm.org/fhir/CodeSystem/acupoints';
            code: string;      // 穴位代码
          }];
        };
      },
      {
        url: 'http://tcm.org/fhir/StructureDefinition/needling-technique';
        valueString: string;   // 针刺手法
      }
    ];
  };
}
```

### 6.2 术语映射表

```typescript
interface TerminologyMapping {
  // ICD-10到中医疾病映射
  icdToTcm: {
    'E11': {  // 2型糖尿病
      tcmDisease: '消渴',
      relatedSyndromes: [
        '肺热津伤证',
        '胃热炽盛证',
        '肾阴亏虚证',
        '阴阳两虚证'
      ],
      commonAcupoints: ['足三里', '三阴交', '肾俞', '脾俞']
    },
    'I10': {  // 原发性高血压
      tcmDisease: '眩晕',
      relatedSyndromes: [
        '肝阳上亢证',
        '肝肾阴虚证',
        '痰湿中阻证',
        '瘀血阻窍证'
      ],
      commonAcupoints: ['太冲', '风池', '曲池', '合谷']
    },
    'K29': {  // 胃炎
      tcmDisease: '胃脘痛',
      relatedSyndromes: [
        '肝胃不和证',
        '脾胃虚寒证',
        '胃阴不足证',
        '瘀血停滞证'
      ],
      commonAcupoints: ['中脘', '足三里', '内关', '公孙']
    }
    // ... 更多映射
  };

  // 西药到中药交互映射
  drugHerbInteractions: {
    'Metformin': {
      interactions: [
        {
          herbs: ['黄芪', '人参', '西洋参'],
          effect: '增强降糖作用',
          management: '监测血糖，必要时调整剂量'
        },
        {
          herbs: ['甘草'],
          effect: '可能影响血糖控制',
          management: '避免大量使用'
        }
      ]
    },
    'Warfarin': {
      interactions: [
        {
          herbs: ['丹参', '当归', '川芎', '红花'],
          effect: '增强抗凝作用，增加出血风险',
          management: '避免同时使用或密切监测INR'
        },
        {
          herbs: ['人参'],
          effect: '可能降低抗凝效果',
          management: '避免同时使用'
        }
      ]
    }
    // ... 更多映射
  };
}
```

---

## 7. 隐私和安全

### 7.1 安全架构

```typescript
interface HIESecurityArchitecture {
  // 传输安全
  transportSecurity: {
    protocol: 'TLS 1.3';
    certificateValidation: true;
    mutualTLS: true;  // 双向认证

    // VPN隧道（可选）
    vpn: {
      enabled: boolean;
      type: 'IPSec' | 'WireGuard';
    };
  };

  // 数据加密
  dataEncryption: {
    // 端到端加密
    e2e: {
      enabled: true;
      algorithm: 'AES-256-GCM';
      keyManagement: 'per-transaction';
    };

    // 字段级加密
    fieldLevel: {
      sensitiveFields: [
        'patient_name',
        'nric',
        'diagnoses',
        'medications'
      ];
    };
  };

  // 访问控制
  accessControl: {
    // 请求者验证
    requesterAuthentication: {
      method: 'OAuth 2.0 + JWT';
      mfa: true;
      practitionerLicenseVerification: true;
    };

    // 患者身份验证
    patientIdentityVerification: {
      methods: ['NRIC', 'MyKad', 'Biometric'];
      threshold: 'high_assurance';
    };

    // 细粒度授权
    fineGrainedAuthorization: {
      basedOn: ['consent', 'role', 'purpose', 'data_type'];
    };
  };

  // 审计
  auditing: {
    // 全面记录
    logging: {
      allRequests: true;
      allResponses: true;
      dataAccess: true;
      dataModification: true;
    };

    // 审计内容
    auditContent: {
      who: 'requester_identity';
      what: 'data_accessed';
      when: 'timestamp';
      where: 'source_ip';
      why: 'purpose';
      how: 'consent_reference';
    };

    // 不可篡改
    tamperProof: {
      method: 'blockchain' | 'signed_logs';
    };
  };

  // 数据最小化
  dataMinimization: {
    // 只返回请求的数据
    filterByRequest: true;

    // 脱敏选项
    deidentification: {
      available: true;
      methods: ['pseudonymization', 'generalization'];
    };
  };
}
```

### 7.2 合规检查清单

```
┌─────────────────────────────────────────────────────────────┐
│  HIE合规检查清单                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📋 患者同意                                                 │
│  ☐ 获取明确书面同意                                          │
│  ☐ 同意书包含所有必要信息                                     │
│  ☐ 提供撤回同意机制                                          │
│  ☐ 记录同意获取过程                                          │
│                                                             │
│  📋 数据安全                                                 │
│  ☐ 传输使用TLS 1.3加密                                       │
│  ☐ 存储使用AES-256加密                                       │
│  ☐ 实施访问控制                                              │
│  ☐ 定期安全审计                                              │
│                                                             │
│  📋 审计追踪                                                 │
│  ☐ 记录所有数据访问                                          │
│  ☐ 审计日志不可篡改                                          │
│  ☐ 日志保留7年                                               │
│  ☐ 定期审计日志审查                                          │
│                                                             │
│  📋 数据主体权利                                              │
│  ☐ 支持患者访问数据                                          │
│  ☐ 支持患者更正数据                                          │
│  ☐ 支持患者撤回同意                                          │
│  ☐ 提供投诉渠道                                              │
│                                                             │
│  📋 机构协议                                                 │
│  ☐ 签订数据共享协议                                          │
│  ☐ 明确责任分配                                              │
│  ☐ 明确数据使用限制                                          │
│  ☐ 明确违规处理流程                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. 数据库设计

### 8.1 HIE相关表结构

```sql
-- 外部数据请求表
CREATE TABLE external_data_requests (
    request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 请求方信息
    requesting_practitioner_id UUID REFERENCES practitioners(practitioner_id),
    requesting_institution VARCHAR(200),

    -- 患者信息
    patient_id UUID REFERENCES patients(patient_id),

    -- 请求内容
    requested_categories TEXT[],
    date_range_from DATE,
    date_range_to DATE,
    source_institutions TEXT[],
    urgency VARCHAR(20),

    -- 同意信息
    consent_id UUID REFERENCES patient_consents(consent_id),

    -- 状态
    status VARCHAR(30),  -- pending, processing, completed, failed, cancelled
    status_message TEXT,

    -- 响应信息
    response_received_at TIMESTAMP,
    records_received INTEGER,
    sources_responded TEXT[],

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 患者同意书表
CREATE TABLE patient_consents (
    consent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID REFERENCES patients(patient_id),

    -- 同意范围
    data_types TEXT[],
    source_institutions TEXT[],
    time_range_from DATE,
    time_range_to DATE,

    -- 有效期
    validity_start DATE,
    validity_end DATE,

    -- 目的
    purpose TEXT,

    -- 签名
    signature_data TEXT,       -- 数字签名或Base64图像
    signed_at TIMESTAMP,
    witness_name VARCHAR(100),
    witness_signature TEXT,

    -- 状态
    status VARCHAR(20),        -- active, revoked, expired
    revoked_at TIMESTAMP,
    revoked_reason TEXT,

    -- 使用记录
    times_used INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 外部病案存储表
CREATE TABLE external_medical_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID REFERENCES patients(patient_id),
    request_id UUID REFERENCES external_data_requests(request_id),

    -- 来源
    source_institution VARCHAR(200),
    source_system VARCHAR(100),

    -- 原始数据
    original_format VARCHAR(20),  -- FHIR, HL7, CDA, PDF
    original_data JSONB,
    original_document BYTEA,      -- PDF/图片等

    -- 解析后数据
    parsed_data JSONB,
    ai_extracted_data JSONB,

    -- 记录类型
    record_type VARCHAR(50),      -- encounter, diagnosis, medication, lab, etc.
    record_date DATE,

    -- 处理状态
    processing_status VARCHAR(20),
    ai_analysis_completed BOOLEAN DEFAULT FALSE,

    -- 医生审阅
    reviewed_by UUID REFERENCES practitioners(practitioner_id),
    reviewed_at TIMESTAMP,
    review_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI整合分析结果表
CREATE TABLE ai_integration_analyses (
    analysis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID REFERENCES patients(patient_id),
    request_id UUID REFERENCES external_data_requests(request_id),

    -- 分析结果
    health_overview JSONB,
    treatment_timeline JSONB,
    current_medications JSONB,
    key_findings JSONB,
    tcm_syndrome_hints JSONB,
    risk_identification JSONB,
    ai_recommendations JSONB,

    -- 元数据
    analysis_version VARCHAR(20),
    confidence_scores JSONB,
    processing_time_ms INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HIE审计日志表
CREATE TABLE hie_audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 事件信息
    event_type VARCHAR(50),       -- request, response, access, export
    event_description TEXT,

    -- 参与方
    requester_id UUID,
    requester_institution VARCHAR(200),
    patient_id UUID,

    -- 数据详情
    data_categories TEXT[],
    records_count INTEGER,

    -- 请求信息
    request_id UUID,
    consent_id UUID,

    -- 技术信息
    source_ip VARCHAR(45),
    user_agent TEXT,

    -- 时间
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 签名（防篡改）
    log_hash VARCHAR(64),
    previous_hash VARCHAR(64)
);

-- 机构连接配置表
CREATE TABLE hie_connections (
    connection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- 机构信息
    institution_name VARCHAR(200),
    institution_type VARCHAR(50),  -- hospital, clinic, lab
    institution_id VARCHAR(100),   -- 机构标识

    -- 连接类型
    connection_type VARCHAR(50),   -- MyHIX, direct, patient_mediated

    -- 技术配置
    endpoint_url TEXT,
    authentication_type VARCHAR(50),
    api_key_encrypted TEXT,
    certificate TEXT,

    -- 能力
    supported_operations TEXT[],   -- query, push, pull
    supported_resources TEXT[],    -- Patient, Encounter, etc.

    -- 状态
    status VARCHAR(20),            -- active, inactive, pending
    last_connected_at TIMESTAMP,
    connection_test_result VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_ext_requests_patient ON external_data_requests(patient_id);
CREATE INDEX idx_ext_requests_status ON external_data_requests(status);
CREATE INDEX idx_consents_patient ON patient_consents(patient_id);
CREATE INDEX idx_consents_status ON patient_consents(status, validity_end);
CREATE INDEX idx_ext_records_patient ON external_medical_records(patient_id);
CREATE INDEX idx_hie_audit_patient ON hie_audit_logs(patient_id);
CREATE INDEX idx_hie_audit_time ON hie_audit_logs(event_timestamp);
```

---

## 9. 界面设计

### 9.1 病案索取主界面

```
┌─────────────────────────────────────────────────────────────┐
│  跨机构病案索取                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  患者: 张三  NRIC: xxxxxx-xx-xxxx                            │
│                                                             │
│  ┌─ 同意状态 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ✅ 有效同意书                                        │   │
│  │  签署日期: 2025-11-01                                 │   │
│  │  有效期至: 2026-11-01                                 │   │
│  │  范围: 所有医疗记录                                    │   │
│  │                                                       │   │
│  │  [查看同意书] [更新同意] [撤销同意]                      │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 发起新请求 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  数据来源:                                            │   │
│  │  ☑ 所有已连接机构                                     │   │
│  │  ☐ 指定机构:                                          │   │
│  │    [中央医院      ] [仁爱诊所      ] [添加...]         │   │
│  │                                                       │   │
│  │  数据类型:                                            │   │
│  │  ☑ 就诊记录  ☑ 诊断  ☑ 用药  ☑ 检验结果               │   │
│  │  ☑ 手术/治疗  ☐ 影像  ☑ 过敏  ☐ 免疫接种               │   │
│  │                                                       │   │
│  │  时间范围:                                            │   │
│  │  [2020-01-01] 至 [2025-11-17]  ☐ 全部历史             │   │
│  │                                                       │   │
│  │  紧急程度: [常规] ▼                                   │   │
│  │                                                       │   │
│  │  [发送请求]                                           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 历史请求 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  请求ID      日期        来源         状态   记录数    │   │
│  │  ─────────────────────────────────────────────────    │   │
│  │  REQ-001    2025-11-15  中央医院+2    ✅完成  23      │   │
│  │  REQ-002    2025-11-10  仁爱诊所      ✅完成  8       │   │
│  │  REQ-003    2025-11-01  所有机构      ⏳处理中 -       │   │
│  │                                                       │   │
│  │  [查看所有] [导出报告]                                 │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ 已整合的外部病案 ───────────────────────────────────┐   │
│  │                                                       │   │
│  │  📊 数据统计:                                         │   │
│  │  • 总记录数: 31条                                     │   │
│  │  • 来源机构: 3个                                      │   │
│  │  • 时间跨度: 2020-03 至 2025-11                       │   │
│  │                                                       │   │
│  │  🔍 AI分析状态: ✅ 已完成                              │   │
│  │                                                       │   │
│  │  [查看完整病案] [查看AI分析] [导入到当前诊疗]           │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 患者上传界面

```
┌─────────────────────────────────────────────────────────────┐
│  患者自行上传病案                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  患者: 张三                                                  │
│                                                             │
│  ┌─ 上传文件 ──────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │                                             │     │   │
│  │  │      📁 拖拽文件到这里，或点击选择文件         │     │   │
│  │  │                                             │     │   │
│  │  │      支持格式: PDF, JPG, PNG, DOCX          │     │   │
│  │  │      最大文件大小: 20MB                      │     │   │
│  │  │                                             │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │                                                       │   │
│  │  已选择文件:                                          │   │
│  │  📄 检验报告_2025-10.pdf (2.3 MB)    [预览] [删除]   │   │
│  │  📄 出院小结.jpg (1.1 MB)            [预览] [删除]   │   │
│  │                                                       │   │
│  │  文件信息 (可选填写，帮助AI更好理解):                   │   │
│  │  来源机构: [中央医院                              ]    │   │
│  │  文件类型: [检验报告] ▼                               │   │
│  │  日期:     [2025-10-15]                               │   │
│  │                                                       │   │
│  │  [上传并AI分析]                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─ AI处理进度 ─────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📄 检验报告_2025-10.pdf                              │   │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%                │   │
│  │  ✅ OCR识别完成                                       │   │
│  │  ✅ 信息提取完成                                       │   │
│  │  ✅ 数据整合完成                                       │   │
│  │                                                       │   │
│  │  提取到的信息:                                        │   │
│  │  • 血糖: 6.8 mmol/L                                  │   │
│  │  • HbA1c: 7.2%                                       │   │
│  │  • 血压: 138/88 mmHg                                 │   │
│  │  • 肝功能: ALT 45 U/L (偏高)                          │   │
│  │                                                       │   │
│  │  [确认正确] [手动修正]                                 │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. 实施建议

### 10.1 分阶段实施

```
阶段1: 基础设施（第1-2月）
├── 同意管理系统
├── 患者上传功能
├── AI文档处理（OCR + NLP）
└── 基本数据库设计

阶段2: 直连集成（第3-4月）
├── 与2-3家合作医院直连
├── FHIR接口开发
├── 数据标准化模块
└── 安全传输通道

阶段3: AI整合分析（第5-6月）
├── 治疗历史分析
├── 中医辨证提示
├── 风险识别
├── 整合报告生成

阶段4: 国家平台集成（第7-8月）
├── MyHIX接入（如果可用）
├── 认证和合规
└── 扩大覆盖范围

阶段5: 优化和扩展（持续）
├── 更多机构接入
├── AI模型优化
└── 用户反馈改进
```

### 10.2 预算估算

| 类别 | 项目 | 预算 (RM) |
|------|------|-----------|
| **开发** | 同意管理系统 | 40,000 |
| | 数据请求/接收模块 | 60,000 |
| | AI文档处理 | 80,000 |
| | AI整合分析 | 100,000 |
| | FHIR接口 | 50,000 |
| | 安全模块 | 60,000 |
| **集成** | 机构对接（每个）| 20,000 x N |
| | MyHIX集成 | 50,000 |
| **合规** | 法律咨询 | 30,000 |
| | 安全审计 | 40,000 |
| **总计（基础）** | | **510,000** |

### 10.3 关键成功因素

1. **患者信任** - 透明的同意流程，清晰的数据使用说明
2. **机构合作** - 与主要医疗机构建立合作关系
3. **数据质量** - 强大的AI处理能力，处理各种格式
4. **安全合规** - 严格遵守PDPA，通过安全认证
5. **医生采纳** - 直观的界面，真正有用的AI分析

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0 | 2025-11-17 | 初始版本 |

---

**文档结束**
