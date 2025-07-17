from django.core.management.base import BaseCommand
from portfolio.models import Resource
import os


class Command(BaseCommand):
    help = 'Populate database with sample resources'

    def handle(self, *args, **options):
        resources_data = [
            {
                'title': 'Modern Dashboard Template',
                'description': 'A sleek, responsive dashboard template built with Tailwind CSS and JavaScript. Perfect for admin panels and data visualization.',
                'category': 'template',
                'file_type': 'ZIP',
                'file_size': '2.1 MB',
                'is_featured': True,
                'tags': 'dashboard, admin, tailwind, responsive, dark mode',
            },
            {
                'title': 'Landing Page Kit',
                'description': 'Complete landing page kit with 10+ sections, hero banners, testimonials, and contact forms.',
                'category': 'template',
                'file_type': 'ZIP',
                'file_size': '4.3 MB',
                'is_featured': True,
                'tags': 'landing page, marketing, bootstrap, responsive',
            },
            {
                'title': 'React Component Library',
                'description': 'Collection of 50+ reusable React components with TypeScript support and Storybook documentation.',
                'category': 'code',
                'file_type': 'ZIP',
                'file_size': '8.7 MB',
                'is_featured': True,
                'tags': 'react, typescript, components, storybook',
            },
            {
                'title': 'Icon Pack - Essential UI',
                'description': 'Set of 200+ minimalist UI icons in SVG format. Includes outline and filled variants.',
                'category': 'image',
                'file_type': 'ZIP',
                'file_size': '1.2 MB',
                'tags': 'icons, svg, ui, design, minimalist',
            },
            {
                'title': 'WordPress Plugin - SEO Toolkit',
                'description': 'Complete SEO plugin for WordPress with meta optimization, sitemap generation, and analytics integration.',
                'category': 'plugin',
                'file_type': 'ZIP',
                'file_size': '3.5 MB',
                'tags': 'wordpress, seo, plugin, analytics',
            },
            {
                'title': 'Database Design Patterns',
                'description': 'Comprehensive guide to database design patterns with real-world examples and best practices.',
                'category': 'document',
                'file_type': 'PDF',
                'file_size': '5.8 MB',
                'tags': 'database, design, patterns, guide, sql',
            },
            {
                'title': 'CSS Animation Library',
                'description': 'Collection of 30+ CSS animations and transitions ready to use in your projects.',
                'category': 'code',
                'file_type': 'CSS',
                'file_size': '120 KB',
                'tags': 'css, animations, transitions, effects',
            },
            {
                'title': 'Mobile App Mockups',
                'description': 'High-quality mobile app mockups for iOS and Android. Includes various screen sizes and orientations.',
                'category': 'image',
                'file_type': 'PSD',
                'file_size': '15.2 MB',
                'tags': 'mockups, mobile, ios, android, design',
            },
            {
                'title': 'E-commerce Template',
                'description': 'Complete e-commerce website template with product pages, shopping cart, and payment integration.',
                'category': 'template',
                'file_type': 'ZIP',
                'file_size': '6.9 MB',
                'tags': 'ecommerce, shopping, template, responsive',
            },
            {
                'title': 'JavaScript Utility Functions',
                'description': 'Collection of commonly used JavaScript utility functions for DOM manipulation, data processing, and more.',
                'category': 'code',
                'file_type': 'JS',
                'file_size': '85 KB',
                'tags': 'javascript, utilities, functions, helpers',
            },
        ]

        created_count = 0
        for resource_data in resources_data:
            resource, created = Resource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created resource: {resource.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Resource already exists: {resource.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new resources!')
        )
