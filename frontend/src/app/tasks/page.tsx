'use client';

import { useState } from 'react';
import {
  Card,
  Form,
  Select,
  InputNumber,
  Button,
  Space,
  Alert,
  Descriptions,
  Tag,
  Spin,
  Divider,
  Typography,
} from 'antd';
import { PlayCircleOutlined, ReloadOutlined } from '@ant-design/icons';
import DashboardLayout from '@/components/DashboardLayout';
import { useSources } from '@/hooks/use-api';
import { taskApi } from '@/lib/api';
import type { TaskRunResponse } from '@/types/api';

const { Title, Text } = Typography;

export default function TasksPage() {
  const [form] = Form.useForm();
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<TaskRunResponse | null>(null);

  const { sources, isLoading: sourcesLoading } = useSources();

  const handleRunTask = async (values: any) => {
    setRunning(true);
    setResult(null);

    try {
      const response = await taskApi.runTask({
        source_id: values.source_id || undefined,
        limit: values.limit || 10,
      });

      setResult(response);
    } catch (error: any) {
      setResult({
        success: false,
        message: error.message || '任务执行失败',
        results: [],
      });
    } finally {
      setRunning(false);
    }
  };

  return (
    <DashboardLayout>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card title="执行采集任务">
          <Form
            form={form}
            layout="vertical"
            onFinish={handleRunTask}
            initialValues={{ limit: 10 }}
          >
            <Form.Item
              label="数据源"
              name="source_id"
              extra="不选择则运行所有启用的数据源"
            >
              <Select
                placeholder="选择数据源（可选）"
                allowClear
                loading={sourcesLoading}
                options={sources?.map((s) => ({
                  label: s.name,
                  value: s.id,
                }))}
              />
            </Form.Item>

            <Form.Item
              label="采集数量"
              name="limit"
              rules={[{ required: true }]}
            >
              <InputNumber min={1} max={100} style={{ width: 200 }} />
            </Form.Item>

            <Form.Item>
              <Space>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<PlayCircleOutlined />}
                  loading={running}
                >
                  {running ? '执行中...' : '开始执行'}
                </Button>
                <Button
                  icon={<ReloadOutlined />}
                  onClick={() => {
                    form.resetFields();
                    setResult(null);
                  }}
                >
                  重置
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Card>

        {running && (
          <Card>
            <Spin tip="任务执行中，请稍候...">
              <div style={{ height: 100 }} />
            </Spin>
          </Card>
        )}

        {result && !running && (
          <Card title="执行结果">
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Alert
                message={result.message}
                type={result.success ? 'success' : 'error'}
                showIcon
              />

              <Divider />

              {result.results.map((r, index) => (
                <Card
                  key={index}
                  size="small"
                  title={
                    <Space>
                      <Text strong>{r.source_name}</Text>
                      {r.error ? (
                        <Tag color="error">失败</Tag>
                      ) : (
                        <Tag color="success">成功</Tag>
                      )}
                    </Space>
                  }
                >
                  {r.error ? (
                    <Text type="danger">错误: {r.error}</Text>
                  ) : (
                    <Descriptions column={2} size="small">
                      <Descriptions.Item label="采集数量">
                        {r.scraped || 0}
                      </Descriptions.Item>
                      <Descriptions.Item label="处理成功">
                        <Text type="success">{r.processed || 0}</Text>
                      </Descriptions.Item>
                      <Descriptions.Item label="已过滤">
                        <Text type="warning">{r.filtered || 0}</Text>
                      </Descriptions.Item>
                      <Descriptions.Item label="错误数">
                        <Text type="danger">{r.errors || 0}</Text>
                      </Descriptions.Item>
                    </Descriptions>
                  )}
                </Card>
              ))}
            </Space>
          </Card>
        )}
      </Space>
    </DashboardLayout>
  );
}
