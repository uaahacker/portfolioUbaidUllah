#!/bin/bash

# Django Portfolio Setup Script
# This script helps you set up the portfolio quickly

echo "🚀 Django Portfolio Setup Script"
echo "================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Populate with sample data
echo "🎨 Populating with sample data..."
python manage.py populate_portfolio

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Start the server: python manage.py runserver"
echo "3. Visit http://127.0.0.1:8000 to see your portfolio"
echo "4. Visit http://127.0.0.1:8000/admin to manage content"
echo ""
echo "📚 Check README.md for detailed documentation"
