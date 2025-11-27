# 招标信息提取系统 - 产品需求文档 (PRD)

| 版本 | 日期 | 作者 | 描述 |
| :--- | :--- | :--- | :--- |
| v1.0 | 2025-11-28 | Antigravity | 初始版本，基于 brains.md 架构设计 |

## 1. 项目概述 (Project Overview)

### 1.1 背景
当前招标信息分散在各个政府网站、企业门户及微信公众号中，格式非结构化（HTML/文本/图片），人工收集和筛选效率极低。

### 1.2 目标
构建一个自动化的情报系统，能够：
1.  **多源采集**：统一采集公开网站、需登录平台及公众号文章。
2.  **智能提取**：利用 LLM (Gemini) 将非结构化文本转化为标准化的 JSON 数据。
3.  **精准过滤**：通过灵活的规则引擎筛选出高价值商机。
4.  **集中管理**：提供统一的 Web 界面进行数据查看和规则配置。

## 2. 用户角色 (User Personas)

*   **系统管理员 (Admin)**: 负责配置爬虫源、管理 Cookie、监控系统运行状态。
*   **业务分析师 (Analyst)**: 负责配置过滤规则、查看招标列表、导出数据。

## 3. 功能需求 (Functional Requirements)

### 3.1 数据采集模块 (Data Acquisition)
*   **REQ-ACQ-01 多源支持**:
    *   支持配置 HTTP GET/POST 请求（针对公开网站）。
    *   支持配置 Playwright 脚本路径（针对复杂动态网站）。
    *   支持微信公众号文章链接的批量导入或自动监听（预留接口）。
*   **REQ-ACQ-02 认证管理**:
    *   提供 Cookie/Session 管理界面。
    *   支持手动更新失效的 Cookie。
    *   支持配置自动保活策略（如每 4 小时访问一次特定 URL）。
*   **REQ-ACQ-03 增量更新**:
    *   系统应记录每个源的最后采集时间或最新文章 ID。
    *   每次任务仅采集新增内容，避免重复处理。

### 3.2 智能提取模块 (AI Extraction)
*   **REQ-EXT-01 结构化提取**:
    *   系统需调用 Gemini API 提取以下核心字段：
        *   `tender_unit` (招标单位)
        *   `project_name` (项目名称)
        *   `project_code` (项目编号)
        *   `budget` (预算金额，统一单位为万元)
        *   `deadline` (投标截止时间，格式 YYYY-MM-DD HH:mm)
        *   `contact_info` (联系人及电话)
*   **REQ-EXT-02 数据清洗与校验**:
    *   自动将金额文本（如“5000元”、“30万”）转换为浮点数。
    *   自动标准化日期格式。
    *   对提取结果进行 Pydantic 校验，格式不符则自动重试或标记错误。
*   **REQ-EXT-03 置信度标记**:
    *   AI 需返回提取置信度 (Confidence Score)。
    *   低于阈值（如 0.8）的数据在前端显示“需复核”标签。

### 3.3 智能过滤模块 (Smart Filtering)
*   **REQ-FIL-01 规则配置**:
    *   支持创建多个过滤规则组。
    *   支持字段级过滤：标题、预算、正文、地区。
    *   支持操作符：包含 (Contains)、不包含 (Excludes)、大于/小于 (Numeric)、正则匹配 (Regex)。
*   **REQ-FIL-02 自动打标**:
    *   符合规则的招标信息自动打上对应标签（如“高价值”、“数据库项目”）。

### 3.4 管理后台 (Management Dashboard)
*   **REQ-UI-01 仪表盘**: 展示今日采集数量、高价值项目数、系统健康状态。
*   **REQ-UI-02 招标列表**:
    *   支持按时间、预算、标签筛选。
    *   支持全文搜索。
    *   列表页显示关键字段摘要。
*   **REQ-UI-03 详情页**:
    *   展示 AI 提取的结构化字段。
    *   展示原文链接及原文快照（Markdown）。
    *   支持人工修正提取错误的字段。
*   **REQ-UI-04 源配置**: 增删改查数据源配置信息。

## 4. 非功能需求 (Non-Functional Requirements)

*   **性能**: 单个采集任务处理时间不超过 5 分钟（含 AI 调用）。
*   **可靠性**: 爬虫失败需支持自动重试（默认 3 次）。
*   **扩展性**: 新增数据源无需修改核心代码，只需增加配置或适配器脚本。
*   **成本**: 优先使用 Gemini 1.5 Flash 模型以控制 Token 成本；对长文本进行预处理裁剪。

## 5. 数据模型 (Data Models)

### 5.1 Tender (招标信息)
```json
{
  "id": "uuid",
  "source_id": "关联的源ID",
  "original_url": "https://...",
  "title": "文章标题",
  "publish_time": "2025-11-28 10:00:00",
  "content_raw": "HTML内容...",
  "content_clean": "Markdown内容...",
  "extracted_data": {
    "budget": 50.0,
    "deadline": "2025-12-01"
  },
  "tags": ["数据库", "金融"],
  "status": "processed / review_required",
  "created_at": "..."
}
```

### 5.2 SourceConfig (源配置)
```json
{
  "id": "uuid",
  "name": "某政府采购网",
  "type": "public / auth / wechat",
  "base_url": "https://...",
  "list_selector": "css selector for list items",
  "content_selector": "css selector for content",
  "cookies": "key=value;...",
  "cron_expression": "0 0 * * *"
}
```

## 6. 实施路线图 (Roadmap)

### Phase 1: MVP (预计 2 周)
*   完成 FastAPI 后端与 PostgreSQL 数据库搭建。
*   实现通用 HTML 采集器 (BaseScraper)。
*   集成 Gemini API 完成核心提取功能。
*   实现基础的关键字过滤。
*   简单的 CLI 或 API 接口进行测试。

### Phase 2: Web 管理端 (预计 2 周)
*   搭建 Next.js + Ant Design Pro 前端。
*   实现招标列表、详情查看、人工修正功能。
*   实现数据源配置界面。

### Phase 3: 高级特性 (预计 3 周)
*   集成 Playwright 处理登录源。
*   实现 Cookie 池管理。
*   对接微信公众号采集方案。
*   完善定时任务与告警。
