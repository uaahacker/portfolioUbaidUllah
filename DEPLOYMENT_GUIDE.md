# Django Portfolio Deployment Guide for Ubuntu

## 📋 Prerequisites
- Ubuntu 20.04+ server
- SSH access to your server
- Domain name (optional but recommended)

## 🔧 Step 1: Server Setup

### Update Ubuntu and Install Dependencies
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install python3 python3-pip python3-venv nginx supervisor git -y

# Install PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib -y
```

### Create Deployment User
```bash
# Create a new user for deployment
sudo adduser deploy
sudo usermod -aG sudo deploy
sudo su - deploy
```

## 🗃️ Step 2: Database Setup (PostgreSQL)

### Configure PostgreSQL
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'your_strong_password';
ALTER ROLE portfolio_user SET client_encoding TO 'utf8';
ALTER ROLE portfolio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE portfolio_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

## 📁 Step 3: Project Deployment

### Clone Your Project
```bash
# Navigate to home directory
cd /home/deploy

# Clone your repository
git clone https://github.com/uaahacker/portfolioUbaidUllah.git
cd portfolioUbaidUllah

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
```bash
# Create .env file
nano .env
```

Add the following content to `.env`:
```env
SECRET_KEY=your-super-secret-key-here-make-it-very-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
DATABASE_URL=postgres://portfolio_user:your_strong_password@localhost:5432/portfolio_db
```

### Configure Django Settings for Production
```bash
# Install additional production packages
pip install psycopg2-binary
```

## ⚙️ Step 4: Django Configuration

### Run Django Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test the application
python manage.py runserver 0.0.0.0:8000
```

## 🌐 Step 5: Nginx Configuration

### Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/portfolio
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        root /home/deploy/portfolioUbaidUllah;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root /home/deploy/portfolioUbaidUllah;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable the Site
```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## 🔄 Step 6: Gunicorn Configuration

### Create Gunicorn Socket
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add the following content:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following content:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/portfolioUbaidUllah
ExecStart=/home/deploy/portfolioUbaidUllah/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          portfolio_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start and Enable Services
```bash
# Start and enable Gunicorn socket
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Check status
sudo systemctl status gunicorn.socket

# Start and enable Gunicorn service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn
```

## 🔒 Step 7: SSL Configuration (Let's Encrypt)

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain SSL Certificate
```bash
# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## 🔥 Step 8: Firewall Configuration

### Configure UFW
```bash
# Enable UFW
sudo ufw enable

# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Check status
sudo ufw status
```

## 📊 Step 9: Monitoring and Maintenance

### Create Deployment Script
```bash
nano /home/deploy/deploy.sh
```

Add the following content:
```bash
#!/bin/bash

# Navigate to project directory
cd /home/deploy/portfolioUbaidUllah

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install any new requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart gunicorn

# Restart Nginx
sudo systemctl restart nginx

echo "Deployment completed successfully!"
```

Make the script executable:
```bash
chmod +x /home/deploy/deploy.sh
```

### Log Monitoring
```bash
# View Gunicorn logs
sudo journalctl -u gunicorn

# View Nginx access logs
sudo tail -f /var/log/nginx/access.log

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## 🚀 Step 10: Final Steps

### Test Your Deployment
1. Visit your domain in a browser
2. Check that all static files load correctly
3. Test the admin panel
4. Verify all portfolio features work

### Regular Maintenance Commands
```bash
# Restart services after code changes
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Check service status
sudo systemctl status gunicorn
sudo systemctl status nginx

# View logs
sudo journalctl -u gunicorn -f
```

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **Permission Errors**:
   ```bash
   sudo chown -R deploy:www-data /home/deploy/portfolioUbaidUllah
   sudo chmod -R 755 /home/deploy/portfolioUbaidUllah
   ```

2. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic --noinput
   sudo systemctl restart nginx
   ```

3. **Database Connection Issues**:
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify database credentials in `.env` file

4. **Gunicorn Not Starting**:
   ```bash
   sudo journalctl -u gunicorn
   # Check the logs for specific errors
   ```

## 📱 Additional Configuration for Your Portfolio

### Media Files Permissions
```bash
sudo chown -R deploy:www-data /home/deploy/portfolioUbaidUllah/media
sudo chmod -R 755 /home/deploy/portfolioUbaidUllah/media
```

### Backup Script
```bash
nano /home/deploy/backup.sh
```

Add backup script content:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/deploy/backups"

mkdir -p $BACKUP_DIR

# Backup database
pg_dump portfolio_db > $BACKUP_DIR/db_backup_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /home/deploy/portfolioUbaidUllah/media

echo "Backup completed: $DATE"
```

Make executable and add to crontab:
```bash
chmod +x /home/deploy/backup.sh
crontab -e
# Add: 0 2 * * * /home/deploy/backup.sh
```

## 🎯 Quick Deployment Checklist

- [ ] Ubuntu server with Python 3.8+
- [ ] PostgreSQL database created
- [ ] Project cloned and virtual environment set up
- [ ] Environment variables configured
- [ ] Django migrations run
- [ ] Static files collected
- [ ] Nginx configured and running
- [ ] Gunicorn service running
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Domain pointing to server
- [ ] Admin user created
- [ ] All features tested

Your Django portfolio should now be live and accessible! 🎉

use discord webhook for conatact us
setup site stats google
update the whole site to ubaid data
setup backup of all the data into postgress and project to gdriveh 
