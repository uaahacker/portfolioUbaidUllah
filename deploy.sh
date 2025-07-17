#!/bin/bash

# Simple deployment script for Ubuntu
echo "🚀 Starting Django Portfolio Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root. Create a deploy user instead."
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install python3 python3-pip python3-venv nginx supervisor git postgresql postgresql-contrib -y

# Create project directory
PROJECT_DIR="/home/$USER/portfolioUbaidUllah"
print_status "Setting up project directory: $PROJECT_DIR"

# Clone repository if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    print_status "Cloning repository..."
    git clone https://github.com/uaahacker/portfolioUbaidUllah.git $PROJECT_DIR
else
    print_warning "Project directory already exists. Pulling latest changes..."
    cd $PROJECT_DIR
    git pull origin main
fi

cd $PROJECT_DIR

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cat > .env << EOF
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    print_warning "Please update the .env file with your production settings!"
fi

# Setup database
print_status "Setting up database..."
python manage.py migrate

# Create superuser (interactive)
print_status "Creating superuser..."
python manage.py createsuperuser

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Set up Gunicorn socket
print_status "Setting up Gunicorn socket..."
sudo tee /etc/systemd/system/gunicorn.socket > /dev/null << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Set up Gunicorn service
print_status "Setting up Gunicorn service..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          portfolio_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn
print_status "Starting Gunicorn service..."
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/portfolio > /dev/null << EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        root $PROJECT_DIR;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root $PROJECT_DIR;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
print_status "Testing and restarting Nginx..."
sudo nginx -t && sudo systemctl restart nginx

# Set proper permissions
print_status "Setting file permissions..."
sudo chown -R $USER:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR

# Configure firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

print_status "🎉 Deployment completed successfully!"
print_warning "Next steps:"
echo "1. Update your .env file with production settings"
echo "2. Configure your domain DNS to point to this server"
echo "3. Install SSL certificate with: sudo certbot --nginx"
echo "4. Test your application at: http://$(curl -s ifconfig.me)"

print_status "Useful commands:"
echo "- Check Gunicorn status: sudo systemctl status gunicorn"
echo "- Check Nginx status: sudo systemctl status nginx"
echo "- View logs: sudo journalctl -u gunicorn -f"
echo "- Restart services: sudo systemctl restart gunicorn nginx"
