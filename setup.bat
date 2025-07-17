@echo off
REM Django Portfolio Setup Script for Windows
REM This script helps you set up the portfolio quickly

echo 🚀 Django Portfolio Setup Script
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️ Running database migrations...
python manage.py migrate

REM Populate with sample data
echo 🎨 Populating with sample data...
python manage.py populate_portfolio

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Start the server: python manage.py runserver
echo 3. Visit http://127.0.0.1:8000 to see your portfolio
echo 4. Visit http://127.0.0.1:8000/admin to manage content
echo.
echo 📚 Check README.md for detailed documentation
pause
