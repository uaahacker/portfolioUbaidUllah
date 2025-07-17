from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import (
    AboutMe, Skill, Project, Technology, ProjectTechnology, 
    Experience, ExperienceTechnology, SiteConfiguration
)
from datetime import date


class Command(BaseCommand):
    help = 'Populate the portfolio with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample portfolio data...'))
        
        # Create or update AboutMe
        about_me, created = AboutMe.objects.get_or_create(
            defaults={
                'name': 'Ubaid Ullah',
                'title': 'Full Stack Developer',
                'bio': '''Hello! I'm Ubaid, a passionate software engineer with over 5 years of experience building innovative digital products. I specialize in creating elegant solutions to complex problems using modern web technologies.

My journey in tech started when I built my first website at 15. Since then, I've worked with startups and established companies to deliver high-quality software solutions that drive business value.

When I'm not coding, you can find me exploring new technologies, contributing to open-source projects, or sharing knowledge with the developer community. I believe in continuous learning and staying at the forefront of technology trends.''',
                'years_experience': 5,
                'location': 'Your Location',
                'email': 'ubaid@example.com',
                'github_url': 'https://github.com/ubaid',
                'linkedin_url': 'https://linkedin.com/in/ubaid',
                'twitter_url': 'https://twitter.com/ubaid',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created AboutMe profile'))
        else:
            self.stdout.write(self.style.WARNING('ℹ AboutMe profile already exists'))
        
        # Create or update SiteConfiguration
        site_config, created = SiteConfiguration.objects.get_or_create(
            defaults={
                'site_title': 'Ubaid Ullah | Portfolio',
                'site_tagline': 'Building the future, one line of code at a time',
                'meta_description': 'Professional portfolio of Ubaid Ullah - Full Stack Developer specializing in modern web technologies',
                'meta_keywords': 'Ubaid Ullah, software engineer, web developer, full stack, portfolio, Django, React, Python',
                'allow_contact_form': True,
                'maintenance_mode': False,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created SiteConfiguration'))
        else:
            self.stdout.write(self.style.WARNING('ℹ SiteConfiguration already exists'))
        
        # Create Technologies
        technologies_data = [
            {'name': 'React', 'color': 'blue', 'icon_class': 'fab fa-react'},
            {'name': 'Django', 'color': 'green', 'icon_class': 'fab fa-python'},
            {'name': 'Python', 'color': 'yellow', 'icon_class': 'fab fa-python'},
            {'name': 'JavaScript', 'color': 'yellow', 'icon_class': 'fab fa-js'},
            {'name': 'TypeScript', 'color': 'blue', 'icon_class': 'fab fa-js'},
            {'name': 'Node.js', 'color': 'green', 'icon_class': 'fab fa-node-js'},
            {'name': 'Vue.js', 'color': 'green', 'icon_class': 'fab fa-vuejs'},
            {'name': 'Angular', 'color': 'red', 'icon_class': 'fab fa-angular'},
            {'name': 'Next.js', 'color': 'gray', 'icon_class': 'fas fa-code'},
            {'name': 'Express.js', 'color': 'gray', 'icon_class': 'fas fa-server'},
            {'name': 'PostgreSQL', 'color': 'blue', 'icon_class': 'fas fa-database'},
            {'name': 'MongoDB', 'color': 'green', 'icon_class': 'fas fa-database'},
            {'name': 'Redis', 'color': 'red', 'icon_class': 'fas fa-database'},
            {'name': 'Docker', 'color': 'blue', 'icon_class': 'fab fa-docker'},
            {'name': 'AWS', 'color': 'orange', 'icon_class': 'fab fa-aws'},
            {'name': 'Git', 'color': 'red', 'icon_class': 'fab fa-git-alt'},
            {'name': 'GraphQL', 'color': 'pink', 'icon_class': 'fas fa-code'},
            {'name': 'REST API', 'color': 'indigo', 'icon_class': 'fas fa-code'},
            {'name': 'Tailwind CSS', 'color': 'teal', 'icon_class': 'fas fa-paint-brush'},
            {'name': 'SASS', 'color': 'pink', 'icon_class': 'fab fa-sass'},
        ]
        
        for tech_data in technologies_data:
            tech, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                self.stdout.write(f'  ✓ Created technology: {tech.name}')
        
        # Create Skills
        skills_data = [
            # Frontend
            {'name': 'React', 'category': 'frontend', 'proficiency': 95, 'icon_class': 'fab fa-react', 'color': 'blue', 'is_featured': True},
            {'name': 'Vue.js', 'category': 'frontend', 'proficiency': 90, 'icon_class': 'fab fa-vuejs', 'color': 'green'},
            {'name': 'JavaScript', 'category': 'frontend', 'proficiency': 95, 'icon_class': 'fab fa-js', 'color': 'yellow'},
            {'name': 'TypeScript', 'category': 'frontend', 'proficiency': 85, 'icon_class': 'fab fa-js', 'color': 'blue'},
            {'name': 'Tailwind CSS', 'category': 'frontend', 'proficiency': 90, 'icon_class': 'fas fa-paint-brush', 'color': 'teal'},
            {'name': 'SASS', 'category': 'frontend', 'proficiency': 85, 'icon_class': 'fab fa-sass', 'color': 'pink'},
            
            # Backend
            {'name': 'Python', 'category': 'backend', 'proficiency': 95, 'icon_class': 'fab fa-python', 'color': 'yellow', 'is_featured': True},
            {'name': 'Django', 'category': 'backend', 'proficiency': 90, 'icon_class': 'fab fa-python', 'color': 'green'},
            {'name': 'Node.js', 'category': 'backend', 'proficiency': 85, 'icon_class': 'fab fa-node-js', 'color': 'green'},
            {'name': 'Express.js', 'category': 'backend', 'proficiency': 80, 'icon_class': 'fas fa-server', 'color': 'gray'},
            {'name': 'GraphQL', 'category': 'backend', 'proficiency': 75, 'icon_class': 'fas fa-code', 'color': 'pink'},
            {'name': 'REST API', 'category': 'backend', 'proficiency': 90, 'icon_class': 'fas fa-code', 'color': 'indigo'},
            
            # Database
            {'name': 'PostgreSQL', 'category': 'database', 'proficiency': 85, 'icon_class': 'fas fa-database', 'color': 'blue'},
            {'name': 'MongoDB', 'category': 'database', 'proficiency': 80, 'icon_class': 'fas fa-database', 'color': 'green'},
            {'name': 'Redis', 'category': 'database', 'proficiency': 75, 'icon_class': 'fas fa-database', 'color': 'red'},
            {'name': 'SQL', 'category': 'database', 'proficiency': 85, 'icon_class': 'fas fa-database', 'color': 'blue'},
            
            # DevOps
            {'name': 'Docker', 'category': 'devops', 'proficiency': 80, 'icon_class': 'fab fa-docker', 'color': 'blue'},
            {'name': 'AWS', 'category': 'devops', 'proficiency': 75, 'icon_class': 'fab fa-aws', 'color': 'orange'},
            {'name': 'CI/CD', 'category': 'devops', 'proficiency': 70, 'icon_class': 'fas fa-cogs', 'color': 'gray'},
            {'name': 'Git', 'category': 'devops', 'proficiency': 90, 'icon_class': 'fab fa-git-alt', 'color': 'red'},
        ]
        
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                category=skill_data['category'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(f'  ✓ Created skill: {skill.name}')
        
        # Create Projects
        projects_data = [
            {
                'title': 'E-Commerce Platform',
                'description': 'A full-featured e-commerce platform with React frontend and Django backend. Features include user authentication, product catalog, shopping cart, payment integration, and admin dashboard.',
                'detailed_description': 'This e-commerce platform was built to demonstrate modern web development practices. It includes a responsive React frontend with Redux for state management, a Django REST API backend, PostgreSQL database, and integrates with Stripe for payments. The platform supports user registration, product browsing, cart management, order processing, and comprehensive admin functionality.',
                'status': 'completed',
                'is_featured': True,
                'start_date': date(2023, 6, 1),
                'end_date': date(2023, 9, 15),
                'github_url': 'https://github.com/ubaid/ecommerce-platform',
                'live_url': 'https://ecommerce-demo.example.com',
                'technologies': ['React', 'Django', 'PostgreSQL', 'Redis', 'Tailwind CSS']
            },
            {
                'title': 'Task Management Dashboard',
                'description': 'A collaborative task management application with real-time updates, team collaboration features, and comprehensive project tracking.',
                'detailed_description': 'This task management dashboard helps teams organize their work efficiently. Built with Vue.js frontend and Node.js backend, it features real-time collaboration using WebSockets, drag-and-drop task management, team messaging, file attachments, and detailed analytics.',
                'status': 'completed',
                'is_featured': False,
                'start_date': date(2023, 3, 1),
                'end_date': date(2023, 5, 30),
                'github_url': 'https://github.com/ubaid/task-manager',
                'live_url': 'https://taskmanager-demo.example.com',
                'technologies': ['Vue.js', 'Node.js', 'MongoDB', 'SASS']
            },
            {
                'title': 'Weather Analytics API',
                'description': 'A RESTful API service that aggregates weather data from multiple sources and provides analytics and forecasting capabilities.',
                'detailed_description': 'This weather analytics API collects data from various weather services and provides comprehensive analytics. Built with Python and FastAPI, it offers real-time weather data, historical analysis, predictive modeling, and custom alerts. The service is containerized with Docker and deployed on AWS.',
                'status': 'completed',
                'is_featured': False,
                'start_date': date(2023, 1, 15),
                'end_date': date(2023, 2, 28),
                'github_url': 'https://github.com/ubaid/weather-api',
                'live_url': 'https://weather-api.example.com',
                'technologies': ['Python', 'PostgreSQL', 'Docker', 'AWS']
            },
            {
                'title': 'Portfolio Website',
                'description': 'A modern, responsive portfolio website built with Django and enhanced with glassmorphism design principles.',
                'detailed_description': 'This portfolio website showcases my work and skills using modern web technologies. Built with Django for the backend and Tailwind CSS for styling, it features a glassmorphism design, smooth animations, responsive layout, and a comprehensive admin interface for content management.',
                'status': 'in_progress',
                'is_featured': False,
                'start_date': date(2024, 1, 1),
                'end_date': None,
                'github_url': 'https://github.com/ubaid/portfolio',
                'live_url': None,
                'technologies': ['Django', 'JavaScript', 'Tailwind CSS', 'PostgreSQL']
            }
        ]
        
        for project_data in projects_data:
            technologies = project_data.pop('technologies', [])
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            
            if created:
                self.stdout.write(f'  ✓ Created project: {project.title}')
                
                # Add technologies to project
                for tech_name in technologies:
                    try:
                        tech = Technology.objects.get(name=tech_name)
                        ProjectTechnology.objects.get_or_create(
                            project=project,
                            technology=tech
                        )
                    except Technology.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'    ⚠ Technology {tech_name} not found'))
        
        # Create Experience
        experiences_data = [
            {
                'job_title': 'Senior Full Stack Developer',
                'company': 'TechNova Solutions',
                'company_url': 'https://technova.example.com',
                'location': 'Remote',
                'description': 'Leading development of enterprise SaaS products using React, Django, and microservices architecture. Implemented CI/CD pipelines reducing deployment time by 40%. Mentored junior developers and established best practices for code quality and testing.',
                'achievements': 'Reduced application load time by 60%\nImplemented automated testing suite increasing code coverage to 95%\nLed migration to microservices architecture\nMentored 5+ junior developers',
                'start_date': date(2021, 6, 1),
                'end_date': None,
                'is_current': True,
                'technologies': ['React', 'Django', 'PostgreSQL', 'Docker', 'AWS']
            },
            {
                'job_title': 'Frontend Developer',
                'company': 'InnovateX',
                'company_url': 'https://innovatex.example.com',
                'location': 'New York, NY',
                'description': 'Developed responsive user interfaces for financial applications serving 100k+ users. Collaborated with UX designers to implement design systems and component libraries. Optimized application performance and implemented accessibility standards.',
                'achievements': 'Built reusable component library used across 10+ projects\nImproved application accessibility score to 98%\nReduced bundle size by 45% through code splitting\nImplemented automated visual regression testing',
                'start_date': date(2019, 3, 1),
                'end_date': date(2021, 5, 31),
                'is_current': False,
                'technologies': ['Vue.js', 'TypeScript', 'SASS', 'Node.js']
            },
            {
                'job_title': 'Junior Full Stack Developer',
                'company': 'DigitalCraft Studios',
                'company_url': 'https://digitalcraft.example.com',
                'location': 'San Francisco, CA',
                'description': 'Built and maintained client websites and web applications using modern web technologies. Contributed to backend development using Python and Django. Participated in agile development processes and code reviews.',
                'achievements': 'Delivered 15+ client projects on time and within budget\nImproved website loading speed by 50% through optimization\nImplemented responsive design for mobile compatibility\nContributed to open-source projects',
                'start_date': date(2017, 8, 1),
                'end_date': date(2019, 2, 28),
                'is_current': False,
                'technologies': ['JavaScript', 'Python', 'Django', 'PostgreSQL']
            }
        ]
        
        for exp_data in experiences_data:
            technologies = exp_data.pop('technologies', [])
            experience, created = Experience.objects.get_or_create(
                job_title=exp_data['job_title'],
                company=exp_data['company'],
                start_date=exp_data['start_date'],
                defaults=exp_data
            )
            
            if created:
                self.stdout.write(f'  ✓ Created experience: {experience.job_title} at {experience.company}')
                
                # Add technologies to experience
                for tech_name in technologies:
                    try:
                        tech = Technology.objects.get(name=tech_name)
                        ExperienceTechnology.objects.get_or_create(
                            experience=experience,
                            technology=tech
                        )
                    except Technology.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'    ⚠ Technology {tech_name} not found'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Sample portfolio data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nNext steps:'))
        self.stdout.write(self.style.SUCCESS('1. Create a superuser: python manage.py createsuperuser'))
        self.stdout.write(self.style.SUCCESS('2. Run the server: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('3. Visit http://127.0.0.1:8000 to see your portfolio'))
        self.stdout.write(self.style.SUCCESS('4. Visit http://127.0.0.1:8000/admin to manage content'))
