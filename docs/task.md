# Task Checklist

## Phase 1: MVP Core (Backend & AI) ✅ COMPLETED
- [x] **Infrastructure Setup**
    - [x] Initialize FastAPI project structure
    - [x] Configure PostgreSQL & ORM
    - [x] Create database tables (`tenders`, `source_configs`)
- [x] **Acquisition Module**
    - [x] Define `BaseScraper` abstract class
    - [x] Implement `SimpleHttpScraper`
    - [x] Create adapter for 1 public website (ccgp.gov.cn)
- [x] **AI Extraction Module**
    - [x] Integrate Gemini API
    - [x] Design Prompt templates (Few-Shot)
    - [x] Implement Pydantic models for validation
    - [x] Implement error retry mechanism
- [x] **Filtering & API**
    - [x] Implement keyword filtering logic
    - [x] Create `run-task` and `get-tenders` APIs
- [x] **Database Migrations**
    - [x] Set up Alembic
- [x] **Testing**
    - [x] Write tests for core modules
- [x] **Documentation & Deployment**
    - [x] Create README with setup instructions
    - [x] Add Docker Compose configuration
    - [x] Add example scripts

## Phase 2: Web Management (Frontend) ✅ COMPLETED
- [x] **Frontend Setup**
    - [x] Initialize Next.js 14 + TypeScript
    - [x] Configure Ant Design 5
    - [x] Set up project structure
    - [x] Configure API client (Axios + SWR)
- [x] **Tender Management**
    - [x] Tender List page with table
    - [x] Search and filter functionality
    - [x] Detail drawer view
    - [x] Manual correction feature
- [x] **Source Configuration**
    - [x] Source list page
    - [x] CRUD operations
    - [x] JSON config editor
    - [x] Filter rules configuration
- [x] **Task Execution**
    - [x] Task execution interface
    - [x] Real-time results display
- [x] **Layout & Navigation**
    - [x] Responsive dashboard layout
    - [x] Side navigation menu
- [x] **Documentation & Deployment**
    - [x] Frontend README
    - [x] Docker configuration
    - [x] Environment setup

## Phase 3: Advanced Features
- [ ] **Advanced Scraper**
    - [ ] Integrate Playwright
    - [ ] Implement Cookie Management
- [ ] **WeChat & Scheduling**
    - [ ] WeChat Official Account Scraper
    - [ ] APScheduler Integration
