'use client';

import { Card, Descriptions, Tag, Typography } from 'antd';
import DashboardLayout from '@/components/DashboardLayout';

const { Title } = Typography;

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <Card title="系统信息">
        <Descriptions column={1} bordered>
          <Descriptions.Item label="系统名称">招标信息管理系统</Descriptions.Item>
          <Descriptions.Item label="版本">v1.0.0 (Phase 2)</Descriptions.Item>
          <Descriptions.Item label="前端框架">Next.js 14 + Ant Design 5</Descriptions.Item>
          <Descriptions.Item label="后端框架">FastAPI + PostgreSQL</Descriptions.Item>
          <Descriptions.Item label="AI 引擎">Google Gemini 2.0</Descriptions.Item>
          <Descriptions.Item label="状态">
            <Tag color="success">运行中</Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </DashboardLayout>
  );
}
