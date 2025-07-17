from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    AboutMe, Skill, Project, Experience, ContactMessage, SiteConfiguration, Resource
)
from .forms import ContactForm
import json


class HomeView(TemplateView):
    template_name = 'portfolio/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create AboutMe instance
        about_me, created = AboutMe.objects.get_or_create(
            defaults={
                'name': 'Your Name',
                'title': 'Software Engineer',
                'bio': 'Passionate software engineer building the future with code.',
            }
        )
        
        # Get featured project
        featured_project = Project.objects.filter(is_featured=True).first()
        
        # Get all projects excluding featured
        projects = Project.objects.filter(
            status='completed'
        ).exclude(
            is_featured=True
        )[:6]  # Limit to 6 projects
        
        # Get skills grouped by category
        skills_by_category = {}
        for skill in Skill.objects.all():
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        
        # Get recent experience
        experiences = Experience.objects.all()[:4]
        
        context.update({
            'about_me': about_me,
            'featured_project': featured_project,
            'projects': projects,
            'skills_by_category': skills_by_category,
            'experiences': experiences,
            'contact_form': ContactForm(),
        })
        
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related projects (same technologies)
        project = self.get_object()
        related_projects = Project.objects.filter(
            technologies__technology__in=[tech.technology for tech in project.technologies.all()]
        ).exclude(id=project.id).distinct()[:3]
        
        context['related_projects'] = related_projects
        return context


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'portfolio/contact.html'
    success_url = '/'
    
    def form_valid(self, form):
        # Add IP address and user agent
        contact_message = form.save(commit=False)
        contact_message.ip_address = self.get_client_ip()
        contact_message.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        contact_message.save()
        
        messages.success(
            self.request, 
            'Thank you for your message! I\'ll get back to you soon.'
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error with your message. Please check the form and try again.'
        )
        return super().form_invalid(form)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


@method_decorator(csrf_exempt, name='dispatch')
class ContactAjaxView(ContactView):
    """AJAX version of contact form for better UX"""
    
    def form_valid(self, form):
        contact_message = form.save(commit=False)
        contact_message.ip_address = self.get_client_ip()
        contact_message.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        contact_message.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! I\'ll get back to you soon.'
        })
    
    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'There was an error with your message. Please check the form and try again.',
            'errors': form.errors
        })
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = ContactForm(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return super().post(request, *args, **kwargs)


class ProjectsView(TemplateView):
    template_name = 'portfolio/projects.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        category = self.request.GET.get('category', '')
        search = self.request.GET.get('search', '')
        
        # Filter projects
        projects = Project.objects.filter(status='completed')
        
        if search:
            projects = projects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(technologies__technology__name__icontains=search)
            ).distinct()
        
        if category:
            projects = projects.filter(technologies__technology__name__iexact=category)
        
        # Pagination
        paginator = Paginator(projects, 9)  # 9 projects per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all technologies for filter buttons
        from .models import Technology
        technologies = Technology.objects.all().order_by('name')
        
        context.update({
            'page_obj': page_obj,
            'technologies': technologies,
            'current_category': category,
            'current_search': search,
        })
        
        return context


class AboutView(TemplateView):
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        about_me, created = AboutMe.objects.get_or_create(
            defaults={
                'name': 'Your Name',
                'title': 'Software Engineer',
                'bio': 'Passionate software engineer building the future with code.',
            }
        )
        
        # Get skills grouped by category
        skills_by_category = {}
        for skill in Skill.objects.all():
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        
        experiences = Experience.objects.all()
        
        context.update({
            'about_me': about_me,
            'skills_by_category': skills_by_category,
            'experiences': experiences,
        })
        
        return context


class ResourcesView(TemplateView):
    template_name = 'portfolio/resources.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Resource
        
        # Get filter parameters
        category_filter = self.request.GET.get('category', 'all')
        search_query = self.request.GET.get('search', '')
        
        # Base queryset
        resources = Resource.objects.all()
        
        # Apply category filter
        if category_filter != 'all':
            resources = resources.filter(category=category_filter)
        
        # Apply search filter
        if search_query:
            resources = resources.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(resources, 12)  # 12 resources per page
        page_number = self.request.GET.get('page')
        resources_page = paginator.get_page(page_number)
        
        # Get categories for filter
        categories = Resource.CATEGORY_CHOICES
        featured_resources = Resource.objects.filter(is_featured=True)[:6]
        
        context.update({
            'resources': resources_page,
            'categories': categories,
            'featured_resources': featured_resources,
            'current_category': category_filter,
            'search_query': search_query,
        })
        
        return context


class ResourceDownloadView(TemplateView):
    def get(self, request, pk):
        from .models import Resource
        from django.http import HttpResponse, Http404
        
        try:
            resource = get_object_or_404(Resource, pk=pk)
            resource.increment_downloads()
            
            if resource.download_url:
                return redirect(resource.download_url)
            elif resource.file:
                return redirect(resource.file.url)
            else:
                raise Http404("File not found")
                
        except Resource.DoesNotExist:
            raise Http404("Resource not found")
