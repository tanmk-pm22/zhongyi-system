from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from accounts.models import User


class Service(models.Model):
    """服务项目 | Service"""

    name_cn = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=200
    )
    name_en = models.CharField(
        _('英文名称 | English Name'),
        max_length=200
    )
    slug = models.SlugField(
        _('URL标识 | URL Slug'),
        unique=True,
        max_length=200
    )
    description_cn = models.TextField(
        _('中文描述 | Chinese Description')
    )
    description_en = models.TextField(
        _('英文描述 | English Description')
    )
    icon = models.CharField(
        _('图标 | Icon'),
        max_length=100,
        help_text='Bootstrap Icon class (e.g., bi-heart-pulse)',
        default='bi-circle'
    )
    image = models.ImageField(
        _('图片 | Image'),
        upload_to='services/',
        blank=True,
        null=True
    )
    price_info_cn = models.CharField(
        _('价格信息（中文） | Price Info (Chinese)'),
        max_length=200,
        blank=True,
        help_text='例如：RM 80 - RM 150'
    )
    price_info_en = models.CharField(
        _('价格信息（英文） | Price Info (English)'),
        max_length=200,
        blank=True,
        help_text='e.g.: RM 80 - RM 150'
    )
    order = models.IntegerField(
        _('排序 | Order'),
        default=0,
        help_text='数字越小越靠前 | Lower numbers appear first'
    )
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )
    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('服务项目 | Service')
        verbose_name_plural = _('服务项目 | Services')
        ordering = ['order', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class ArticleCategory(models.Model):
    """文章分类 | Article Category"""

    name_cn = models.CharField(
        _('中文名称 | Chinese Name'),
        max_length=100
    )
    name_en = models.CharField(
        _('英文名称 | English Name'),
        max_length=100
    )
    slug = models.SlugField(
        _('URL标识 | URL Slug'),
        unique=True,
        max_length=100
    )
    order = models.IntegerField(
        _('排序 | Order'),
        default=0
    )
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )
    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('文章分类 | Article Category')
        verbose_name_plural = _('文章分类 | Article Categories')
        ordering = ['order', 'name_cn']

    def __str__(self):
        return f"{self.name_cn} | {self.name_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


class Article(models.Model):
    """健康文章 | Health Article"""

    title_cn = models.CharField(
        _('中文标题 | Chinese Title'),
        max_length=300
    )
    title_en = models.CharField(
        _('英文标题 | English Title'),
        max_length=300
    )
    slug = models.SlugField(
        _('URL标识 | URL Slug'),
        unique=True,
        max_length=300
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name=_('分类 | Category')
    )
    summary_cn = models.TextField(
        _('中文摘要 | Chinese Summary'),
        blank=True,
        help_text='简短摘要，用于列表页显示'
    )
    summary_en = models.TextField(
        _('英文摘要 | English Summary'),
        blank=True,
        help_text='Brief summary for list pages'
    )
    content_cn = models.TextField(
        _('中文内容 | Chinese Content')
    )
    content_en = models.TextField(
        _('英文内容 | English Content')
    )
    featured_image = models.ImageField(
        _('特色图片 | Featured Image'),
        upload_to='articles/',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name=_('作者 | Author'),
        limit_choices_to={'role__in': ['admin', 'practitioner']}
    )
    published_date = models.DateTimeField(
        _('发布日期 | Published Date'),
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        _('已发布 | Published'),
        default=False
    )
    is_featured = models.BooleanField(
        _('精选 | Featured'),
        default=False,
        help_text='精选文章会显示在首页 | Featured articles appear on homepage'
    )
    views_count = models.IntegerField(
        _('浏览次数 | Views Count'),
        default=0
    )
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )
    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('健康文章 | Article')
        verbose_name_plural = _('健康文章 | Articles')
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return f"{self.title_cn} | {self.title_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def increment_views(self):
        """增加浏览次数 | Increment views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Testimonial(models.Model):
    """患者评价 | Patient Testimonial"""

    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ (5)'),
        (4, '⭐⭐⭐⭐ (4)'),
        (3, '⭐⭐⭐ (3)'),
        (2, '⭐⭐ (2)'),
        (1, '⭐ (1)'),
    ]

    patient_name = models.CharField(
        _('患者姓名 | Patient Name'),
        max_length=100,
        help_text='可以使用化名 | Can use pseudonym'
    )
    content_cn = models.TextField(
        _('评价内容（中文） | Content (Chinese)'),
        blank=True
    )
    content_en = models.TextField(
        _('评价内容（英文） | Content (English)'),
        blank=True
    )
    rating = models.IntegerField(
        _('评分 | Rating'),
        choices=RATING_CHOICES,
        default=5
    )
    service_received = models.CharField(
        _('接受的服务 | Service Received'),
        max_length=200,
        blank=True
    )
    testimonial_date = models.DateField(
        _('评价日期 | Testimonial Date'),
        auto_now_add=True
    )
    is_approved = models.BooleanField(
        _('已审核 | Approved'),
        default=False,
        help_text='只有审核通过的评价才会显示在网站上 | Only approved testimonials appear on website'
    )
    is_featured = models.BooleanField(
        _('精选 | Featured'),
        default=False,
        help_text='精选评价会显示在首页 | Featured testimonials appear on homepage'
    )
    order = models.IntegerField(
        _('排序 | Order'),
        default=0
    )
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )
    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('患者评价 | Testimonial')
        verbose_name_plural = _('患者评价 | Testimonials')
        ordering = ['-is_featured', 'order', '-testimonial_date']

    def __str__(self):
        return f"{self.patient_name} - {'⭐' * self.rating} ({self.testimonial_date})"


class ClinicInfo(models.Model):
    """诊所信息 | Clinic Information"""

    clinic_name_cn = models.CharField(
        _('诊所名称（中文） | Clinic Name (Chinese)'),
        max_length=200
    )
    clinic_name_en = models.CharField(
        _('诊所名称（英文） | Clinic Name (English)'),
        max_length=200
    )
    tagline_cn = models.CharField(
        _('标语（中文） | Tagline (Chinese)'),
        max_length=300,
        blank=True
    )
    tagline_en = models.CharField(
        _('标语（英文） | Tagline (English)'),
        max_length=300,
        blank=True
    )
    about_cn = models.TextField(
        _('关于我们（中文） | About Us (Chinese)'),
        blank=True
    )
    about_en = models.TextField(
        _('关于我们（英文） | About Us (English)'),
        blank=True
    )
    address = models.TextField(
        _('地址 | Address')
    )
    phone = models.CharField(
        _('电话 | Phone'),
        max_length=50
    )
    email = models.EmailField(
        _('邮箱 | Email'),
        blank=True
    )
    business_hours_cn = models.TextField(
        _('营业时间（中文） | Business Hours (Chinese)'),
        help_text='例如：周一至周六 9:00-18:00'
    )
    business_hours_en = models.TextField(
        _('营业时间（英文） | Business Hours (English)'),
        help_text='e.g.: Mon-Sat 9:00-18:00'
    )
    google_maps_embed = models.TextField(
        _('Google地图嵌入代码 | Google Maps Embed Code'),
        blank=True,
        help_text='从Google Maps复制iframe代码 | Copy iframe code from Google Maps'
    )
    facebook_url = models.URLField(
        _('Facebook链接 | Facebook URL'),
        blank=True
    )
    instagram_url = models.URLField(
        _('Instagram链接 | Instagram URL'),
        blank=True
    )
    whatsapp_number = models.CharField(
        _('WhatsApp号码 | WhatsApp Number'),
        max_length=50,
        blank=True,
        help_text='包含国家代码，例如：60123456789'
    )
    wechat_id = models.CharField(
        _('微信号 | WeChat ID'),
        max_length=100,
        blank=True
    )
    logo = models.ImageField(
        _('诊所Logo | Clinic Logo'),
        upload_to='clinic/',
        blank=True,
        null=True
    )
    hero_image = models.ImageField(
        _('首页主图 | Hero Image'),
        upload_to='clinic/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _('启用 | Active'),
        default=True
    )
    created_at = models.DateTimeField(
        _('创建时间 | Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('更新时间 | Updated At'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('诊所信息 | Clinic Information')
        verbose_name_plural = _('诊所信息 | Clinic Information')

    def __str__(self):
        return f"{self.clinic_name_cn} | {self.clinic_name_en}"

    def save(self, *args, **kwargs):
        # 确保只有一条诊所信息记录 | Ensure only one clinic info record exists
        if not self.pk and ClinicInfo.objects.exists():
            raise ValueError('只能有一条诊所信息记录 | Only one clinic info record allowed')
        super().save(*args, **kwargs)
