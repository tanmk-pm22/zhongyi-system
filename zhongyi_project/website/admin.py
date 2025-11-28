from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Service, ArticleCategory, Article, Testimonial, ClinicInfo


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'name_en', 'icon', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_cn', 'name_en', 'description_cn', 'description_en')
    ordering = ('order', 'name_cn')
    prepopulated_fields = {'slug': ('name_en',)}

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('name_cn', 'name_en', 'slug', 'icon', 'image', 'order')
        }),
        (_('描述 | Description'), {
            'fields': ('description_cn', 'description_en')
        }),
        (_('价格信息 | Price Information'), {
            'fields': ('price_info_cn', 'price_info_en')
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'name_en', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_cn', 'name_en')
    ordering = ('order', 'name_cn')
    prepopulated_fields = {'slug': ('name_en',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title_cn', 'title_en', 'category', 'author', 'is_published', 'is_featured', 'views_count', 'published_date')
    list_filter = ('is_published', 'is_featured', 'category', 'published_date', 'created_at')
    search_fields = ('title_cn', 'title_en', 'content_cn', 'content_en')
    ordering = ('-published_date', '-created_at')
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published_date'

    fieldsets = (
        (_('基本信息 | Basic Information'), {
            'fields': ('title_cn', 'title_en', 'slug', 'category', 'author', 'featured_image')
        }),
        (_('摘要 | Summary'), {
            'fields': ('summary_cn', 'summary_en')
        }),
        (_('内容 | Content'), {
            'fields': ('content_cn', 'content_en')
        }),
        (_('发布设置 | Publishing Settings'), {
            'fields': ('is_published', 'is_featured', 'published_date')
        }),
        (_('统计 | Statistics'), {
            'fields': ('views_count',)
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )

    readonly_fields = ('views_count',)

    def save_model(self, request, obj, form, change):
        # 如果是新建且未设置作者，自动设置为当前用户
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'rating', 'service_received', 'is_approved', 'is_featured', 'testimonial_date')
    list_filter = ('is_approved', 'is_featured', 'rating', 'testimonial_date')
    search_fields = ('patient_name', 'content_cn', 'content_en', 'service_received')
    ordering = ('-is_featured', 'order', '-testimonial_date')
    date_hierarchy = 'testimonial_date'

    fieldsets = (
        (_('患者信息 | Patient Information'), {
            'fields': ('patient_name', 'service_received')
        }),
        (_('评价内容 | Testimonial Content'), {
            'fields': ('content_cn', 'content_en', 'rating')
        }),
        (_('显示设置 | Display Settings'), {
            'fields': ('is_approved', 'is_featured', 'order')
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )

    actions = ['approve_testimonials', 'disapprove_testimonials', 'mark_as_featured']

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, _(f'{updated} 条评价已审核通过 | {updated} testimonials approved'))
    approve_testimonials.short_description = _('审核通过选中的评价 | Approve selected testimonials')

    def disapprove_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, _(f'{updated} 条评价已取消审核 | {updated} testimonials disapproved'))
    disapprove_testimonials.short_description = _('取消审核选中的评价 | Disapprove selected testimonials')

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, _(f'{updated} 条评价已设为精选 | {updated} testimonials marked as featured'))
    mark_as_featured.short_description = _('设为精选 | Mark as featured')


@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ('clinic_name_cn', 'clinic_name_en', 'phone', 'email', 'is_active')

    fieldsets = (
        (_('诊所名称 | Clinic Name'), {
            'fields': ('clinic_name_cn', 'clinic_name_en', 'tagline_cn', 'tagline_en')
        }),
        (_('关于我们 | About Us'), {
            'fields': ('about_cn', 'about_en')
        }),
        (_('联系信息 | Contact Information'), {
            'fields': ('address', 'phone', 'email')
        }),
        (_('营业时间 | Business Hours'), {
            'fields': ('business_hours_cn', 'business_hours_en')
        }),
        (_('地图 | Map'), {
            'fields': ('google_maps_embed',)
        }),
        (_('社交媒体 | Social Media'), {
            'fields': ('facebook_url', 'instagram_url', 'whatsapp_number', 'wechat_id')
        }),
        (_('图片 | Images'), {
            'fields': ('logo', 'hero_image')
        }),
        (_('状态 | Status'), {
            'fields': ('is_active',)
        }),
    )

    def has_add_permission(self, request):
        # 限制只能有一条诊所信息记录
        if ClinicInfo.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # 不允许删除诊所信息
        return False
