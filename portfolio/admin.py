from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    AboutMe, Skill, Project, Technology, ProjectTechnology,
    Experience, ExperienceTechnology, ContactMessage, SiteConfiguration
)


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'years_experience', 'updated_at']
    fields = [
        'name', 'title', 'bio', 'profile_image', 'resume_file',
        'years_experience', 'location', 'email', 'phone',
        'github_url', 'linkedin_url', 'twitter_url'
    ]
    
    def has_add_permission(self, request):
        # Prevent adding if an instance already exists
        return not AboutMe.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon_class']
    list_filter = ['color']
    search_fields = ['name']
    ordering = ['name']


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1
    autocomplete_fields = ['technology']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'created_at', 'get_technologies']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [ProjectTechnologyInline]
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'detailed_description', 'thumbnail')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_technologies(self, obj):
        return ', '.join([tech.technology.name for tech in obj.technologies.all()[:3]])
    get_technologies.short_description = 'Technologies'
    
    def get_thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">',
                obj.thumbnail.url
            )
        return "No image"
    get_thumbnail_preview.short_description = 'Preview'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured', 'color']
    list_filter = ['category', 'is_featured', 'color']
    search_fields = ['name']
    list_editable = ['proficiency', 'is_featured']
    ordering = ['category', '-proficiency']


class ExperienceTechnologyInline(admin.TabularInline):
    model = ExperienceTechnology
    extra = 1
    autocomplete_fields = ['technology']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'start_date', 'end_date', 'is_current', 'get_duration']
    list_filter = ['is_current', 'start_date']
    search_fields = ['job_title', 'company', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    inlines = [ExperienceTechnologyInline]
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'company', 'company_url', 'location')
        }),
        ('Description', {
            'fields': ('description', 'achievements')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_duration(self, obj):
        return obj.duration
    get_duration.short_description = 'Duration'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'user_agent', 'created_at']
    list_editable = ['is_read', 'is_replied']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'replied_at')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        # Messages are created through the contact form
        return False
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_replied(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_replied=True, replied_at=timezone.now())
        self.message_user(request, f'{queryset.count()} messages marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'maintenance_mode', 'allow_contact_form', 'updated_at']
    fields = [
        'site_title', 'site_tagline', 'meta_description', 'meta_keywords',
        'google_analytics_id', 'maintenance_mode', 'allow_contact_form'
    ]
    
    def has_add_permission(self, request):
        # Prevent adding if an instance already exists
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


# Customize the admin site
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"
