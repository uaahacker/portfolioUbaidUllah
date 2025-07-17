# Django Portfolio Website 🚀

A modern, futuristic portfolio website built with Django and enhanced with glassmorphism design principles. Features a fully functional admin interface for easy content management.

![Portfolio Preview](https://via.placeholder.com/800x400/1e293b/ffffff?text=Portfolio+Preview)

## ✨ Features

### 🎨 Frontend
- **Glassmorphism Design**: Modern frosted glass aesthetic with backdrop blur effects
- **Responsive Layout**: Mobile-first design that looks great on all devices
- **Smooth Animations**: AOS (Animate On Scroll) animations for engaging user experience
- **Dark/Light Mode**: Theme toggle with system preference detection
- **Interactive Elements**: Hover effects, smooth scrolling, and micro-interactions

### 🔧 Backend
- **Django Admin**: Full admin interface for content management
- **Dynamic Content**: All content is database-driven and easily manageable
- **Contact Form**: AJAX-powered contact form with spam protection
- **SEO Optimized**: Meta tags, Open Graph tags, and semantic HTML
- **Security**: CSRF protection, secure headers, and input validation

### 📊 Content Management
- **About Me**: Personal information, bio, and social links
- **Projects**: Portfolio projects with technologies, links, and descriptions
- **Skills**: Categorized skills with proficiency levels
- **Experience**: Professional timeline with achievements
- **Contact Messages**: Admin interface to manage inquiries

## 🛠 Tech Stack

### Backend
- **Django 5.x**: Web framework
- **Python 3.8+**: Programming language
- **SQLite/PostgreSQL**: Database
- **Pillow**: Image processing
- **WhiteNoise**: Static file serving

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icons
- **AOS**: Animate on scroll library
- **Vanilla JavaScript**: Interactive features

### Additional
- **Crispy Forms**: Form rendering
- **Python Decouple**: Environment variables
- **Gunicorn**: WSGI server (production)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd portfolioUbaid
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the values as needed

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create sample data** (optional)
   ```bash
   python manage.py populate_portfolio
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit your portfolio**
   - Frontend: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

## 📁 Project Structure

```
portfolioUbaid/
├── portfolio/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── admin.py              # Admin configuration
│   ├── forms.py              # Form definitions
│   ├── urls.py               # URL routing
│   └── management/           # Custom commands
├── portfolio_project/        # Django project settings
├── templates/                # HTML templates
│   └── portfolio/
├── static/                   # Static files
│   ├── css/
│   ├── js/
│   └── img/
├── media/                    # User uploads
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                # This file
```

## 🎯 Usage

### Admin Interface

1. **Login to Admin**: Visit `/admin` and login with your superuser credentials

2. **Manage Content**:
   - **About Me**: Update personal information and bio
   - **Projects**: Add/edit portfolio projects
   - **Skills**: Manage technical skills by category
   - **Experience**: Add work experience timeline
   - **Technologies**: Manage technology tags
   - **Contact Messages**: View and respond to inquiries
   - **Site Configuration**: Update site-wide settings

### Customization

#### Adding New Projects
1. Go to Admin → Projects → Add Project
2. Fill in project details, description, and links
3. Add relevant technologies
4. Set as featured for homepage display

#### Managing Skills
1. Go to Admin → Skills → Add Skill
2. Choose category (Frontend, Backend, DevOps, etc.)
3. Set proficiency level (1-100)
4. Add Font Awesome icon class if needed

#### Updating Personal Info
1. Go to Admin → About Me
2. Update bio, contact info, and social links
3. Upload profile image and resume

## 🎨 Customization

### Colors and Styling
- Edit the Tailwind config in `templates/portfolio/base.html`
- Modify glassmorphism effects in the CSS section
- Update color schemes in the admin for skills and technologies

### Adding New Sections
1. Create new models in `models.py`
2. Add admin configuration in `admin.py`
3. Update views in `views.py`
4. Create templates in `templates/portfolio/`

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-portfolio-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-domain.herokuapp.com"
   ```

4. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### DigitalOcean/VPS Deployment

1. **Setup server with Ubuntu**
2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx postgresql
   ```

3. **Clone and setup project**
4. **Configure Gunicorn and Nginx**
5. **Setup SSL certificate with Let's Encrypt**

## 🔒 Security Features

- CSRF protection on all forms
- XSS protection headers
- Secure file upload handling
- Input validation and sanitization
- Rate limiting on contact form
- Secure static file serving

## 📱 Responsive Design

The portfolio is fully responsive and optimized for:
- 📱 Mobile devices (320px+)
- 📱 Tablets (768px+)
- 💻 Laptops (1024px+)
- 🖥️ Desktops (1280px+)

## 🎪 Demo

Check out the live demo: [Your Portfolio URL]

Admin credentials for demo:
- Username: demo
- Password: demo123

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Tailwind CSS for the utility-first CSS framework
- Font Awesome for the beautiful icons
- AOS library for smooth animations
- Django community for the amazing framework

## 📞 Support

If you have any questions or need help with setup, feel free to:
- Open an issue on GitHub
- Contact me at [your-email@example.com]

---

**Made with ❤️ using Django and Tailwind CSS**
