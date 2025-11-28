#!/bin/bash
# Quick setup script for Phase 1 MVP

set -e

echo "🚀 Tender Scraper - Phase 1 Setup"
echo "=================================="

# Check Python version
echo "✓ Checking Python version..."
python3 --version | grep -q "3.10\|3.11\|3.12" || {
    echo "❌ Python 3.10+ required"
    exit 1
}

# Navigate to backend
cd "$(dirname "$0")/backend"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env from example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your GEMINI_API_KEY"
    echo ""
fi

# Check if PostgreSQL is running
echo "✓ Checking PostgreSQL..."
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. Please install Docker or set up PostgreSQL manually."
else
    # Check if container exists
    if ! docker ps -a | grep -q tender-postgres; then
        echo "✓ Starting PostgreSQL container..."
        docker run -d \
            --name tender-postgres \
            -e POSTGRES_PASSWORD=postgres \
            -e POSTGRES_DB=tender_scraper \
            -p 5432:5432 \
            postgres:16
        echo "⏳ Waiting for PostgreSQL to be ready..."
        sleep 5
    elif ! docker ps | grep -q tender-postgres; then
        echo "✓ Starting existing PostgreSQL container..."
        docker start tender-postgres
        sleep 3
    else
        echo "✓ PostgreSQL already running"
    fi
fi

# Run tests
echo "✓ Running tests..."
pytest tests/ -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env and add your GEMINI_API_KEY"
echo "  2. Run migrations: cd backend && alembic revision --autogenerate -m 'Initial' && alembic upgrade head"
echo "  3. Start server: python -m uvicorn app.main:app --reload"
echo "  4. Visit http://localhost:8000/docs"
echo ""
