"""
Models for TCM Constitution Analysis (中医体质辨识).
Based on the 9 Constitution Types classification system.
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class ConstitutionType(models.Model):
    """
    Nine TCM Constitution Types (九种体质类型).

    Based on Wang Qi's 9 Constitution Classification:
    1. 平和质 (Balanced)
    2. 气虚质 (Qi Deficiency)
    3. 阳虚质 (Yang Deficiency)
    4. 阴虚质 (Yin Deficiency)
    5. 痰湿质 (Phlegm-Dampness)
    6. 湿热质 (Damp-Heat)
    7. 血瘀质 (Blood Stasis)
    8. 气郁质 (Qi Stagnation)
    9. 特禀质 (Special Diathesis)
    """

    name_cn = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=50,
        unique=True,
    )

    name_en = models.CharField(
        _('英文名称 | English Name'),
        max_length=100,
    )

    code = models.CharField(
        _('编码 | Code'),
        max_length=20,
        unique=True,
    )

    description = models.TextField(
        _('描述 | Description'),
        help_text=_('详细描述体质特点 | Detailed description of constitution characteristics'),
    )

    # Physical Characteristics
    physical_features = models.TextField(
        _('形体特征 | Physical Features'),
        blank=True,
    )

    # Common Symptoms
    common_symptoms = models.TextField(
        _('常见表现 | Common Symptoms'),
        blank=True,
    )

    # Psychological Characteristics
    psychological_features = models.TextField(
        _('心理特征 | Psychological Features'),
        blank=True,
    )

    # Susceptibility to Diseases
    disease_susceptibility = models.TextField(
        _('易患疾病 | Disease Susceptibility'),
        blank=True,
    )

    # Adaptation to Environment
    environmental_adaptation = models.TextField(
        _('环境适应性 | Environmental Adaptation'),
        blank=True,
    )

    # Health Recommendations
    dietary_recommendations = models.TextField(
        _('饮食建议 | Dietary Recommendations'),
        blank=True,
    )

    lifestyle_recommendations = models.TextField(
        _('生活起居建议 | Lifestyle Recommendations'),
        blank=True,
    )

    exercise_recommendations = models.TextField(
        _('运动建议 | Exercise Recommendations'),
        blank=True,
    )

    herbal_recommendations = models.TextField(
        _('药膳建议 | Herbal Food Therapy'),
        blank=True,
    )

    # Display order
    display_order = models.IntegerField(
        _('显示顺序 | Display Order'),
        default=0,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('体质类型 | Constitution Type')
        verbose_name_plural = _('体质类型 | Constitution Types')
        ordering = ['display_order', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"


class ConstitutionQuestionnaire(models.Model):
    """
    Questionnaire for constitution assessment.
    体质辨识问卷题目
    """

    constitution_type = models.ForeignKey(
        ConstitutionType,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('体质类型 | Constitution Type'),
    )

    question_text = models.TextField(
        _('问题 | Question'),
    )

    question_number = models.IntegerField(
        _('题号 | Question Number'),
    )

    # Scoring guide
    scoring_guide = models.JSONField(
        _('评分指南 | Scoring Guide'),
        default=dict,
        blank=True,
        help_text=_('得分说明：1=没有(不会), 2=很少, 3=有时, 4=经常, 5=总是'),
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('体质问卷题目 | Constitution Question')
        verbose_name_plural = _('体质问卷题目 | Constitution Questions')
        ordering = ['constitution_type', 'question_number']
        unique_together = ['constitution_type', 'question_number']

    def __str__(self):
        return f"Q{self.question_number}: {self.question_text[:50]}..."


class ConstitutionAssessment(models.Model):
    """
    Constitution assessment for a patient.
    患者体质辨识评估记录
    """

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='constitution_assessments',
        verbose_name=_('患者 | Patient'),
    )

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='constitution_assessments',
        verbose_name=_('医师 | Practitioner'),
    )

    assessment_date = models.DateTimeField(
        _('评估日期 | Assessment Date'),
        auto_now_add=True,
    )

    # Primary and Secondary Constitution Types
    primary_constitution = models.ForeignKey(
        ConstitutionType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='primary_assessments',
        verbose_name=_('主要体质 | Primary Constitution'),
    )

    primary_score = models.DecimalField(
        _('主要体质得分 | Primary Score'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    secondary_constitution = models.ForeignKey(
        ConstitutionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='secondary_assessments',
        verbose_name=_('次要体质 | Secondary Constitution'),
    )

    secondary_score = models.DecimalField(
        _('次要体质得分 | Secondary Score'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    # Detailed scores for all 9 types
    scores = models.JSONField(
        _('各体质得分 | All Constitution Scores'),
        default=dict,
        help_text=_('存储9种体质的得分 | Stores scores for all 9 constitution types'),
    )

    # AI Analysis
    ai_analysis = models.TextField(
        _('AI分析 | AI Analysis'),
        blank=True,
        help_text=_('AI-generated constitution analysis and recommendations'),
    )

    # Custom Notes
    practitioner_notes = models.TextField(
        _('医师备注 | Practitioner Notes'),
        blank=True,
    )

    # Recommendations
    health_recommendations = models.TextField(
        _('健康建议 | Health Recommendations'),
        blank=True,
    )

    # Follow-up
    follow_up_date = models.DateField(
        _('复评日期 | Follow-up Date'),
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(_('启用 | Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('体质评估 | Constitution Assessment')
        verbose_name_plural = _('体质评估 | Constitution Assessments')
        ordering = ['-assessment_date']

    def __str__(self):
        primary = self.primary_constitution.name_cn if self.primary_constitution else 'N/A'
        return f"{self.patient.full_name} - {primary} ({self.assessment_date.strftime('%Y-%m-%d')})"

    def calculate_constitution_scores(self, answers):
        """
        Calculate constitution scores based on questionnaire answers.
        根据问卷答案计算体质得分

        Args:
            answers: Dict with question_id as key and score (1-5) as value
        """
        from collections import defaultdict

        constitution_scores = defaultdict(list)

        # Group answers by constitution type
        for question_id, score in answers.items():
            try:
                question = ConstitutionQuestionnaire.objects.get(id=question_id)
                constitution_scores[question.constitution_type.code].append(score)
            except ConstitutionQuestionnaire.DoesNotExist:
                continue

        # Calculate average scores for each constitution type
        final_scores = {}
        for const_code, scores_list in constitution_scores.items():
            if scores_list:
                # Convert to percentage (1-5 scale to 0-100)
                avg_score = sum(scores_list) / len(scores_list)
                percentage = ((avg_score - 1) / 4) * 100  # Normalize to 0-100
                final_scores[const_code] = round(percentage, 2)

        self.scores = final_scores

        # Determine primary and secondary constitutions
        if final_scores:
            sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

            # Primary constitution
            primary_code, primary_score = sorted_scores[0]
            self.primary_constitution = ConstitutionType.objects.get(code=primary_code)
            self.primary_score = primary_score

            # Secondary constitution (if significantly high)
            if len(sorted_scores) > 1 and sorted_scores[1][1] >= 40:
                secondary_code, secondary_score = sorted_scores[1]
                self.secondary_constitution = ConstitutionType.objects.get(code=secondary_code)
                self.secondary_score = secondary_score

        self.save()
        return final_scores


class ConstitutionAssessmentAnswer(models.Model):
    """
    Individual answers to constitution questionnaire.
    问卷答案记录
    """

    assessment = models.ForeignKey(
        ConstitutionAssessment,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('评估 | Assessment'),
    )

    question = models.ForeignKey(
        ConstitutionQuestionnaire,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('问题 | Question'),
    )

    score = models.IntegerField(
        _('得分 | Score'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('1=没有, 2=很少, 3=有时, 4=经常, 5=总是'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('问卷答案 | Assessment Answer')
        verbose_name_plural = _('问卷答案 | Assessment Answers')
        unique_together = ['assessment', 'question']

    def __str__(self):
        return f"{self.assessment.patient.full_name} - Q{self.question.question_number}: {self.score}"
