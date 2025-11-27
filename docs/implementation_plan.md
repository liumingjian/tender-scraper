# 招标信息提取系统 - 实施计划 (Implementation Plan)

本文档基于 `prd.md` 将项目拆分为三个阶段，每个阶段包含详细的开发目标、任务分解、技术规范及验收标准。

## Phase 1: MVP 核心链路 (Core Backend & AI)
**目标**: 跑通“采集 -> 提取 -> 存储”核心流程，实现对公开网站的招标信息结构化入库。

### 1.1 开发任务
*   **基础框架搭建**
    *   [ ] 初始化 FastAPI 项目结构 (routers, models, services, utils)。
    *   [ ] 配置 PostgreSQL 数据库及 SQLAlchemy/Tortoise ORM。
    *   [ ] 设计并创建数据库表: `tenders`, `source_configs`。
*   **采集模块 (Acquisition)**
    *   [ ] 定义 `BaseScraper` 抽象基类。
    *   [ ] 实现 `SimpleHttpScraper` (基于 `httpx` + `BeautifulSoup`)。
    *   [ ] 编写 1 个示例公开招标网站的采集适配器。
*   **AI 提取模块 (Extraction)**
    *   [ ] 集成 Google Gemini API。
    *   [ ] 设计 Prompt 模板 (包含 Few-Shot 示例)。
    *   [ ] 实现 Pydantic 模型 `TenderExtractModel` 用于校验和清洗数据。
    *   [ ] 实现提取服务的错误重试机制。
*   **规则过滤 (Filtering)**
    *   [ ] 实现基础的关键字过滤逻辑 (Title/Content contains/excludes)。
*   **API 接口**
    *   [ ] `POST /api/v1/run-task`: 手动触发采集任务。
    *   [ ] `GET /api/v1/tenders`: 获取招标信息列表 (支持基础筛选)。

### 1.2 技术规范
*   **Python 版本**: 3.10+
*   **代码风格**: 遵循 PEP 8，使用 `black` 格式化，`ruff` 进行 Lint 检查。
*   **类型提示**: 全面使用 Python Type Hints。
*   **数据库**: 使用 Alembic 进行数据库版本迁移管理。
*   **AI 模型**: 默认使用 `gemini-1.5-flash`。

### 1.3 验收标准 (Acceptance Criteria)
1.  **功能**: 能成功运行脚本，采集指定网站的最新 10 条招标公告。
2.  **准确性**: 核心字段 (金额、截止时间) 提取准确率 > 90% (人工抽检)。
3.  **存储**: 采集结果正确写入 PostgreSQL，且无重复数据。
4.  **接口**: `/api/v1/tenders` 能返回 JSON 格式数据。

---

## Phase 2: Web 管理后台 (Frontend & Management)
**目标**: 提供可视化的管理界面，允许用户查看数据、配置规则和管理数据源。

### 2.1 开发任务
*   **前端框架搭建**
    *   [ ] 初始化 Next.js + Ant Design Pro 项目。
    *   [ ] 配置 Axios/SWR 请求库及后端 API 代理。
*   **招标列表页**
    *   [ ] 实现分页表格展示招标信息。
    *   [ ] 实现多条件搜索 (时间范围、预算区间、关键词)。
    *   [ ] 实现详情抽屉/弹窗，展示 Markdown 格式的原文及提取结果。
*   **数据源配置页**
    *   [ ] 实现数据源的 CRUD 界面。
    *   [ ] 支持在线测试采集规则 (Dry Run)。
*   **规则配置页**
    *   [ ] 设计 JSON/YAML 编辑器或可视化表单配置过滤规则。
*   **人工修正**
    *   [ ] 在详情页允许编辑 AI 提取的字段，并保存修正记录。

### 2.2 技术规范
*   **前端框架**: Next.js 14 (App Router), TypeScript, Tailwind CSS。
*   **组件库**: Ant Design 5.x。
*   **状态管理**: Zustand 或 React Context。

### 2.3 验收标准 (Acceptance Criteria)
1.  **交互**: 用户能在 3 步内完成一条新过滤规则的配置。
2.  **展示**: 列表页加载时间 < 1秒。
3.  **修正**: 修改详情页的“预算”字段后，数据库对应记录同步更新。

---

## Phase 3: 高级采集与增强 (Advanced Features)
**目标**: 攻克复杂数据源 (登录/微信)，完善系统的自动化与稳定性。

### 3.1 开发任务
*   **复杂采集 (Playwright)**
    *   [ ] 集成 Playwright (Python)。
    *   [ ] 实现 `BrowserScraper`，支持 JavaScript 渲染页面。
    *   [ ] 实现 Cookie 注入与自动保活逻辑。
*   **微信公众号采集**
    *   [ ] 搭建独立服务或集成第三方 API 获取公众号文章链接。
    *   [ ] 对接采集流程。
*   **任务调度**
    *   [ ] 集成 APScheduler。
    *   [ ] 实现定时任务配置 (Cron 表达式)。
    *   [ ] 实现任务失败告警 (Log/Webhook)。
*   **系统优化**
    *   [ ] 引入 Redis 缓存热点查询。
    *   [ ] 优化 Docker Compose 部署配置。

### 3.2 技术规范
*   **浏览器**: Headless Chromium。
*   **并发**: 控制 Playwright 并发数，避免被封禁。
*   **安全**: 敏感信息 (Cookie, API Key) 必须加密存储或通过环境变量注入。

### 3.3 验收标准 (Acceptance Criteria)
1.  **覆盖率**: 能成功采集至少 1 个需要登录的网站。
2.  **自动化**: 设置定时任务后，系统能每天自动运行并产出新数据。
3.  **稳定性**: 连续运行 7 天无崩溃。
