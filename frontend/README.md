# Tender Scraper - Frontend

Next.js 14 + Ant Design Pro 前端管理系统

## 功能特性

✅ **招标信息管理**
- 分页表格展示
- 多条件搜索（关键词、数据源、预算区间）
- 详情抽屉查看
- 在线编辑与人工修正
- Markdown 正文渲染

✅ **数据源配置**
- CRUD 操作
- 在线测试采集规则
- 过滤规则配置

✅ **任务执行**
- 手动触发采集任务
- 实时结果展示

## 技术栈

- **框架**: Next.js 14 (App Router)
- **UI库**: Ant Design 5.x + Ant Design Pro Components
- **状态管理**: SWR (数据获取) + Zustand (全局状态)
- **HTTP客户端**: Axios
- **语言**: TypeScript
- **样式**: CSS Modules + Ant Design Token

## 项目结构

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # 根布局
│   │   ├── page.tsx            # 首页（重定向）
│   │   ├── tenders/            # 招标信息页面
│   │   ├── sources/            # 数据源管理
│   │   ├── tasks/              # 任务执行
│   │   └── settings/           # 系统设置
│   ├── components/             # 组件
│   │   └── DashboardLayout.tsx # 主布局
│   ├── lib/                    # 工具库
│   │   ├── api-client.ts       # Axios 配置
│   │   └── api.ts              # API 服务层
│   ├── hooks/                  # 自定义 Hooks
│   │   └── use-api.ts          # SWR Hooks
│   └── types/                  # TypeScript 类型
│       └── api.ts              # API 类型定义
├── public/                     # 静态资源
├── package.json
├── tsconfig.json
├── next.config.js
└── .env.local.example
```

## 安装

```bash
cd frontend

# 安装依赖
npm install
# 或
yarn install
# 或
pnpm install
```

## 配置

创建 `.env.local` 文件：

```bash
cp .env.local.example .env.local
```

编辑 `.env.local`：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 运行

### 开发模式

```bash
npm run dev
```

访问 [http://localhost:3000](http://localhost:3000)

### 生产构建

```bash
npm run build
npm start
```

## 主要页面

### 1. 招标信息列表 (`/tenders`)

**功能**:
- 表格展示所有招标信息
- 搜索: 关键词、数据源、预算区间
- 查看详情 (Drawer)
- 在线编辑提取字段
- 标记人工修正

**关键组件**:
- `TenderTable` - 表格组件
- `TenderDetail` - 详情抽屉
- `TenderForm` - 编辑表单

### 2. 数据源管理 (`/sources`)

**功能**:
- 列表展示所有数据源
- 新建/编辑/删除数据源
- 配置采集规则 (CSS Selectors)
- 配置过滤规则 (关键词、预算)
- 在线测试连接

**配置项**:
```typescript
{
  name: "数据源名称",
  url: "基础URL",
  scraper_type: "http" | "browser",
  config: {
    list_url: "列表页URL",
    list_selector: "CSS选择器",
    title_selector: "标题选择器",
    url_selector: "链接选择器",
    content_selector: "内容选择器"
  },
  filter_rules: {
    include_keywords: ["关键词"],
    exclude_keywords: ["排除词"],
    min_budget: 100000,
    max_budget: 5000000
  }
}
```

### 3. 任务执行 (`/tasks`)

**功能**:
- 选择数据源
- 设置采集数量
- 执行任务
- 查看实时结果

## API 集成

### Hooks 使用

```typescript
import { useTenders, useSources } from '@/hooks/use-api';

// 获取招标列表
const { tenders, isLoading, mutate } = useTenders({
  keyword: '软件',
  min_budget: 100000
});

// 获取数据源列表
const { sources, isLoading } = useSources();
```

### 直接调用 API

```typescript
import { tenderApi, sourceApi, taskApi } from '@/lib/api';

// 更新招标
await tenderApi.updateTender(id, { budget_amount: 500000 });

// 创建数据源
await sourceApi.createSource({ ... });

// 执行任务
const result = await taskApi.runTask({ source_id: 1, limit: 10 });
```

## 开发指南

### 添加新页面

1. 在 `src/app/` 下创建目录
2. 创建 `page.tsx`
3. 使用 `DashboardLayout` 包裹
4. 更新导航菜单

### 添加新 API

1. 在 `src/types/api.ts` 定义类型
2. 在 `src/lib/api.ts` 添加方法
3. 在 `src/hooks/use-api.ts` 创建 Hook（可选）

### 样式定制

编辑 `src/app/layout.tsx` 中的 ConfigProvider 配置：

```typescript
<ConfigProvider
  theme={{
    token: {
      colorPrimary: '#1890ff',
      borderRadius: 6,
      // 更多 Token...
    },
  }}
>
```

## 部署

### Vercel (推荐)

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel
```

### Docker

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

## 常见问题

### 1. API 连接失败

检查 `.env.local` 中的 `NEXT_PUBLIC_API_URL` 是否正确，确保后端服务正在运行。

### 2. 样式不生效

确保正确导入了 Ant Design 样式，检查 `layout.tsx` 中的 `AntdRegistry`。

### 3. TypeScript 错误

运行 `npm run type-check` 检查类型错误。

## 性能优化

- ✅ SWR 自动缓存与重新验证
- ✅ Next.js 自动代码分割
- ✅ 图片优化 (next/image)
- ✅ 按需加载组件

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## License

MIT
