# Task Checklist

## Phase 1: MVP Core (Backend & AI)
- [ ] **Infrastructure Setup**
    - [ ] Initialize FastAPI project structure
    - [ ] Configure PostgreSQL & ORM
    - [ ] Create database tables (`tenders`, `source_configs`)
- [ ] **Acquisition Module**
    - [ ] Define `BaseScraper` abstract class
    - [ ] Implement `SimpleHttpScraper`
    - [ ] Create adapter for 1 public website
- [ ] **AI Extraction Module**
    - [ ] Integrate Gemini API
    - [ ] Design Prompt templates (Few-Shot)
    - [ ] Implement Pydantic models for validation
    - [ ] Implement error retry mechanism
- [ ] **Filtering & API**
    - [ ] Implement keyword filtering logic
    - [ ] Create `run-task` and `get-tenders` APIs

## Phase 2: Web Management (Frontend)
- [ ] **Frontend Setup**
    - [ ] Initialize Next.js + Ant Design Pro
- [ ] **Features**
    - [ ] Tender List & Detail View
    - [ ] Source Configuration
    - [ ] Rule Configuration
    - [ ] Manual Correction

## Phase 3: Advanced Features
- [ ] **Advanced Scraper**
    - [ ] Integrate Playwright
    - [ ] Implement Cookie Management
- [ ] **WeChat & Scheduling**
    - [ ] WeChat Official Account Scraper
    - [ ] APScheduler Integration
