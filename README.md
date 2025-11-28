# Tender Information Extraction System (招标信息提取系统)

## 简介
这是一个自动化的通用招标信息获取系统，旨在从公开网站、需登录平台及微信公众号等多种渠道采集数据，利用 LLM (Gemini) 进行非结构化数据的精准提取，并通过语义分析实现智能推送。

## 文档索引
*   [技术架构方案 (Architecture)](./docs/brains.md)
*   [产品需求文档 (PRD)](./docs/prd.md)
*   [实施计划 (Implementation Plan)](./docs/implementation_plan.md)
*   [任务清单 (Task Checklist)](./docs/task.md)

## 快速开始

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 16 (or use Docker)
- Google Gemini API Key

### Option 1: Docker Compose (推荐)

```bash
# 1. 设置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，添加你的 GEMINI_API_KEY

# 2. 启动所有服务（后端 + 前端 + 数据库）
docker-compose up -d

# 3. 访问应用
open http://localhost:3000        # 前端界面
open http://localhost:8000/docs   # API 文档
```

### Option 2: 本地开发

**后端**:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 编辑 .env，添加你的 GEMINI_API_KEY

# 启动 PostgreSQL
docker run -d --name tender-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=tender_scraper \
  -p 5432:5432 postgres:16

# 运行数据库迁移
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 启动后端服务
python -m uvicorn app.main:app --reload
```

**前端**:
```bash
cd frontend
npm install

cp .env.local.example .env.local
# 编辑 .env.local，设置 API_URL

# 启动前端服务
npm run dev
```

### 测试运行

```bash
# 后端测试
cd backend
python example_scrape.py
pytest

# 前端类型检查
cd frontend
npm run type-check
```

详细文档:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## 当前进度

✅ **Phase 1: MVP Core (Backend & AI)** - 已完成
- 核心采集模块 (HTTP Scraper)
- AI 提取模块 (Gemini 2.0)
- 过滤规则系统
- RESTful API
- 数据库设计与迁移
- 测试套件

✅ **Phase 2: Web Management (Frontend)** - 已完成
- Next.js 14 + Ant Design 5 界面
- 招标信息列表与详情
- 多条件搜索与过滤
- 在线编辑与人工修正
- 数据源配置管理
- 任务执行界面

⏳ **Phase 3: Advanced Features** - 待开始
- Playwright 浏览器采集
- 微信公众号采集
- APScheduler 定时调度

## 功能截图

### 招标信息管理
- 表格列表展示
- 关键词/预算搜索
- 详情抽屉查看
- 在线编辑修正

### 数据源配置
- 新建/编辑/删除数据源
- JSON 配置采集规则
- 过滤规则设置

### 任务执行
- 选择数据源
- 实时执行结果
- 统计数据展示
