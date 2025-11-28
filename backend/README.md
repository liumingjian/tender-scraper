# Tender Scraper - Backend

FastAPI backend for scraping and extracting tender announcements.

## Features

- ✅ Async scraping with httpx + BeautifulSoup
- ✅ AI extraction with Google Gemini
- ✅ PostgreSQL database with SQLAlchemy
- ✅ RESTful API with FastAPI
- ✅ Keyword & budget filtering
- ✅ Database migrations with Alembic
- ✅ Comprehensive test suite

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 4. Set Up Database

```bash
# Start PostgreSQL (using Docker)
docker run -d \
  --name tender-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tender_scraper \
  -p 5432:5432 \
  postgres:16

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 5. Run Server

```bash
# Development mode
python -m uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API will be available at [http://localhost:8000](http://localhost:8000)

API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Usage

### Run Example Scraper

```bash
python example_scrape.py
```

### Create a Data Source

```bash
curl -X POST http://localhost:8000/api/v1/sources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "中国政府采购网",
    "url": "http://www.ccgp.gov.cn",
    "scraper_type": "http",
    "config": {
      "list_url": "http://www.ccgp.gov.cn/cggg/dfgg/",
      "list_selector": "ul.vT-srch-result-list-bid > li",
      "title_selector": "a",
      "url_selector": "a",
      "content_selector": "div.vF_detail_content"
    },
    "filter_rules": {
      "exclude_keywords": ["废标", "流标"],
      "min_budget": 100000
    }
  }'
```

### Run Scraping Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks/run \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": 1,
    "limit": 10
  }'
```

### Get Tenders

```bash
# Get all non-filtered tenders
curl http://localhost:8000/api/v1/tenders

# Search by keyword
curl "http://localhost:8000/api/v1/tenders?keyword=软件&min_budget=50000"
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_filter.py -v
```

## Code Quality

```bash
# Format code
black app tests

# Lint code
ruff check app tests

# Type checking
mypy app
```

## API Endpoints

### Tenders
- `GET /api/v1/tenders` - List tenders (with filtering)
- `GET /api/v1/tenders/{id}` - Get tender details
- `PATCH /api/v1/tenders/{id}` - Update tender (manual correction)

### Sources
- `POST /api/v1/sources` - Create data source
- `GET /api/v1/sources` - List sources
- `GET /api/v1/sources/{id}` - Get source details
- `PATCH /api/v1/sources/{id}` - Update source
- `DELETE /api/v1/sources/{id}` - Delete source

### Tasks
- `POST /api/v1/tasks/run` - Run scraping task

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   │   ├── scraper/     # Scraping services
│   │   └── ai/          # AI extraction
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── tests/               # Test suite
├── alembic/             # Database migrations
└── requirements.txt     # Dependencies
```

## License

MIT
