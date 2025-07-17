from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone
from PIL import Image
import os


class AboutMe(models.Model):
    """Single instance model for about me section"""
    name = models.CharField(max_length=100, default="Alex Morgan")
    title = models.CharField(max_length=150, default="Software Engineer")
    bio = models.TextField(help_text="Your bio description")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Me"
        verbose_name_plural = "About Me"

    def __str__(self):
        return f"{self.name} - {self.title}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and AboutMe.objects.exists():
            raise ValueError('Only one AboutMe instance is allowed')
        return super().save(*args, **kwargs)

    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return '/static/img/default-avatar.jpg'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('design', 'UI/UX Design'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Font Awesome class like 'fab fa-react'"
    )
    proficiency = models.IntegerField(
        default=80, 
        help_text="Proficiency level from 1-100"
    )
    color = models.CharField(
        max_length=20, 
        default="indigo", 
        help_text="Tailwind color name"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', '-proficiency', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    detailed_description = models.TextField(blank=True, help_text="Longer description for project detail page")
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Featured projects appear in the 'Current Project' section")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return '/static/img/default-project.jpg'

    @property
    def stack_list(self):
        return self.technologies.all()


class Technology(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default="blue", help_text="Tailwind color name")
    icon_class = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['project', 'technology']
        verbose_name = "Project Technology"
        verbose_name_plural = "Project Technologies"


class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    achievements = models.TextField(blank=True, help_text="Key achievements (one per line)")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current job")
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.job_title} at {self.company}"

    @property
    def duration(self):
        end = self.end_date or timezone.now().date()
        start = self.start_date
        years = (end - start).days // 365
        months = ((end - start).days % 365) // 30
        
        if years > 0:
            return f"{years}y {months}m" if months > 0 else f"{years}y"
        else:
            return f"{months}m" if months > 0 else "< 1m"

    @property
    def tools_list(self):
        return self.tools.all()


class ExperienceTechnology(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='tools')
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['experience', 'technology']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_replied(self):
        self.is_replied = True
        self.replied_at = timezone.now()
        self.save()


class SiteConfiguration(models.Model):
    """Single instance model for site-wide settings"""
    site_title = models.CharField(max_length=100, default="Portfolio")
    site_tagline = models.CharField(max_length=200, default="Building the future, one line of code at a time")
    meta_description = models.TextField(
        max_length=160, 
        default="Professional portfolio website showcasing my skills and projects"
    )
    meta_keywords = models.CharField(
        max_length=255, 
        default="software engineer, web developer, portfolio"
    )
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)
    allow_contact_form = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValueError('Only one SiteConfiguration instance is allowed')
        return super().save(*args, **kwargs)
