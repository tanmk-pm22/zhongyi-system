from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Service, Article, ArticleCategory, Testimonial, ClinicInfo
from accounts.models import User
from acupuncture.models import AcupointReference
from prescriptions.models import Herb, ClassicFormula


def get_clinic_info():
    """获取诊所信息 | Get clinic information"""
    try:
        return ClinicInfo.objects.filter(is_active=True).first()
    except ClinicInfo.DoesNotExist:
        return None


def home(request):
    """首页 | Homepage"""
    context = {
        'clinic_info': get_clinic_info(),
        'services': Service.objects.filter(is_active=True)[:4],  # Top 4 services
        'featured_articles': Article.objects.filter(
            is_published=True,
            is_featured=True,
            is_active=True
        )[:3],
        'testimonials': Testimonial.objects.filter(
            is_approved=True,
            is_featured=True,
            is_active=True
        )[:6],
        'practitioners': User.objects.filter(
            role='practitioner',
            is_active=True
        )[:3],
    }
    return render(request, 'website/home.html', context)


def about(request):
    """关于我们 | About Us"""
    context = {
        'clinic_info': get_clinic_info(),
        'practitioners': User.objects.filter(
            role='practitioner',
            is_active=True
        ),
        'testimonials': Testimonial.objects.filter(
            is_approved=True,
            is_active=True
        )[:10],
    }
    return render(request, 'website/about.html', context)


def services_list(request):
    """服务列表 | Services List"""
    services = Service.objects.filter(is_active=True)
    context = {
        'clinic_info': get_clinic_info(),
        'services': services,
    }
    return render(request, 'website/services_list.html', context)


def service_detail(request, slug):
    """服务详情 | Service Detail"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(id=service.id)[:3]

    context = {
        'clinic_info': get_clinic_info(),
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'website/service_detail.html', context)


def practitioners_list(request):
    """医师列表 | Practitioners List"""
    practitioners = User.objects.filter(
        role='practitioner',
        is_active=True
    )

    # 搜索功能 | Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        practitioners = practitioners.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )

    context = {
        'clinic_info': get_clinic_info(),
        'practitioners': practitioners,
        'search_query': search_query,
    }
    return render(request, 'website/practitioners_list.html', context)


def practitioner_detail(request, pk):
    """医师详情 | Practitioner Detail"""
    practitioner = get_object_or_404(
        User,
        pk=pk,
        role='practitioner',
        is_active=True
    )

    context = {
        'clinic_info': get_clinic_info(),
        'practitioner': practitioner,
    }
    return render(request, 'website/practitioner_detail.html', context)


def knowledge_home(request):
    """知识库首页 | Knowledge Base Home"""
    context = {
        'clinic_info': get_clinic_info(),
        'acupoint_count': AcupointReference.objects.filter(is_active=True).count(),
        'herb_count': Herb.objects.filter(is_active=True).count(),
        'formula_count': ClassicFormula.objects.filter(is_active=True).count(),
        'article_count': Article.objects.filter(
            is_published=True,
            is_active=True
        ).count(),
        'recent_articles': Article.objects.filter(
            is_published=True,
            is_active=True
        )[:6],
    }
    return render(request, 'website/knowledge_home.html', context)


def acupoints_list(request):
    """穴位列表 | Acupoints List"""
    acupoints = AcupointReference.objects.filter(is_active=True)

    # 按经络筛选 | Filter by meridian
    meridian = request.GET.get('meridian', '')
    if meridian:
        acupoints = acupoints.filter(meridian=meridian)

    # 搜索功能 | Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        acupoints = acupoints.filter(
            Q(code__icontains=search_query) |
            Q(chinese_name__icontains=search_query) |
            Q(pinyin_name__icontains=search_query) |
            Q(english_name__icontains=search_query) |
            Q(indications__icontains=search_query)
        )

    # 分页 | Pagination
    paginator = Paginator(acupoints, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取所有经络类型 | Get all meridian types
    meridian_choices = AcupointReference.MERIDIAN_CHOICES

    context = {
        'clinic_info': get_clinic_info(),
        'page_obj': page_obj,
        'meridian_choices': meridian_choices,
        'selected_meridian': meridian,
        'search_query': search_query,
    }
    return render(request, 'website/acupoints_list.html', context)


def acupoint_detail(request, code):
    """穴位详情 | Acupoint Detail"""
    acupoint = get_object_or_404(
        AcupointReference,
        code=code.upper(),
        is_active=True
    )

    # 增加使用次数 | Increment usage count
    acupoint.increment_usage()

    # 相关穴位（同经络）| Related acupoints (same meridian)
    related_acupoints = AcupointReference.objects.filter(
        meridian=acupoint.meridian,
        is_active=True
    ).exclude(code=acupoint.code)[:5]

    context = {
        'clinic_info': get_clinic_info(),
        'acupoint': acupoint,
        'related_acupoints': related_acupoints,
    }
    return render(request, 'website/acupoint_detail.html', context)


def herbs_list(request):
    """中药列表 | Herbs List"""
    herbs = Herb.objects.filter(is_active=True)

    # 按性味归经筛选 | Filter by nature, taste, meridian
    nature = request.GET.get('nature', '')
    taste = request.GET.get('taste', '')

    if nature:
        herbs = herbs.filter(nature=nature)
    if taste:
        herbs = herbs.filter(tastes__contains=taste)

    # 搜索功能 | Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        herbs = herbs.filter(
            Q(code__icontains=search_query) |
            Q(name_cn__icontains=search_query) |
            Q(name_en__icontains=search_query) |
            Q(name_pinyin__icontains=search_query) |
            Q(functions__icontains=search_query) |
            Q(indications__icontains=search_query)
        )

    # 分页 | Pagination
    paginator = Paginator(herbs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取性味选项 | Get nature and taste choices
    nature_choices = Herb.NATURE_CHOICES
    taste_choices = Herb.TASTE_CHOICES

    context = {
        'clinic_info': get_clinic_info(),
        'page_obj': page_obj,
        'nature_choices': nature_choices,
        'taste_choices': taste_choices,
        'selected_nature': nature,
        'selected_taste': taste,
        'search_query': search_query,
    }
    return render(request, 'website/herbs_list.html', context)


def herb_detail(request, pk):
    """中药详情 | Herb Detail"""
    herb = get_object_or_404(Herb, pk=pk, is_active=True)

    # 相关中药（同类别）| Related herbs (same category)
    related_herbs = Herb.objects.filter(
        category=herb.category,
        is_active=True
    ).exclude(id=herb.id)[:5]

    context = {
        'clinic_info': get_clinic_info(),
        'herb': herb,
        'related_herbs': related_herbs,
    }
    return render(request, 'website/herb_detail.html', context)


def formulas_list(request):
    """方剂列表 | Formulas List"""
    formulas = ClassicFormula.objects.filter(is_active=True)

    # 搜索功能 | Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        formulas = formulas.filter(
            Q(code__icontains=search_query) |
            Q(name_cn__icontains=search_query) |
            Q(name_en__icontains=search_query) |
            Q(name_pinyin__icontains=search_query) |
            Q(functions__icontains=search_query) |
            Q(indications__icontains=search_query)
        )

    # 分页 | Pagination
    paginator = Paginator(formulas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clinic_info': get_clinic_info(),
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'website/formulas_list.html', context)


def formula_detail(request, pk):
    """方剂详情 | Formula Detail"""
    formula = get_object_or_404(ClassicFormula, pk=pk, is_active=True)

    # 获取方剂组成 | Get formula composition
    formula_herbs = formula.formula_herbs.all().select_related('herb')

    context = {
        'clinic_info': get_clinic_info(),
        'formula': formula,
        'formula_herbs': formula_herbs,
    }
    return render(request, 'website/formula_detail.html', context)


def articles_list(request):
    """文章列表 | Articles List"""
    articles = Article.objects.filter(
        is_published=True,
        is_active=True
    )

    # 按分类筛选 | Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    # 搜索功能 | Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        articles = articles.filter(
            Q(title_cn__icontains=search_query) |
            Q(title_en__icontains=search_query) |
            Q(summary_cn__icontains=search_query) |
            Q(summary_en__icontains=search_query) |
            Q(content_cn__icontains=search_query) |
            Q(content_en__icontains=search_query)
        )

    # 分页 | Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取所有分类 | Get all categories
    categories = ArticleCategory.objects.filter(is_active=True)

    context = {
        'clinic_info': get_clinic_info(),
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'website/articles_list.html', context)


def article_detail(request, slug):
    """文章详情 | Article Detail"""
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True,
        is_active=True
    )

    # 增加浏览次数 | Increment views
    article.increment_views()

    # 相关文章（同分类）| Related articles (same category)
    related_articles = Article.objects.filter(
        category=article.category,
        is_published=True,
        is_active=True
    ).exclude(id=article.id)[:3]

    context = {
        'clinic_info': get_clinic_info(),
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'website/article_detail.html', context)


def contact(request):
    """联系我们 | Contact Us"""
    if request.method == 'POST':
        # 处理联系表单 | Handle contact form
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        # TODO: 发送邮件或保存到数据库 | Send email or save to database
        # For now, just show a success message
        messages.success(
            request,
            _('感谢您的留言！我们会尽快与您联系。| Thank you for your message! We will contact you soon.')
        )
        return redirect('website:contact')

    context = {
        'clinic_info': get_clinic_info(),
    }
    return render(request, 'website/contact.html', context)
