'use client';

import { useState } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  Switch,
  message,
  Card,
  Tag,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import DashboardLayout from '@/components/DashboardLayout';
import { useSources } from '@/hooks/use-api';
import { sourceApi } from '@/lib/api';
import type { SourceConfig, SourceConfigCreate } from '@/types/api';

const { TextArea } = Input;

export default function SourcesPage() {
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSource, setEditingSource] = useState<SourceConfig | null>(null);
  const [form] = Form.useForm();

  const { sources, isLoading, mutate } = useSources();

  const handleCreate = () => {
    setEditingSource(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: SourceConfig) => {
    setEditingSource(record);
    form.setFieldsValue({
      ...record,
      config: JSON.stringify(record.config, null, 2),
      filter_rules: record.filter_rules ? JSON.stringify(record.filter_rules, null, 2) : '',
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个数据源吗？',
      onOk: async () => {
        try {
          await sourceApi.deleteSource(id);
          message.success('删除成功');
          mutate();
        } catch (error) {
          message.error('删除失败');
        }
      },
    });
  };

  const handleSubmit = async (values: any) => {
    try {
      const payload: SourceConfigCreate = {
        ...values,
        config: JSON.parse(values.config),
        filter_rules: values.filter_rules ? JSON.parse(values.filter_rules) : undefined,
      };

      if (editingSource) {
        await sourceApi.updateSource(editingSource.id, payload);
        message.success('更新成功');
      } else {
        await sourceApi.createSource(payload);
        message.success('创建成功');
      }

      setModalVisible(false);
      mutate();
    } catch (error) {
      message.error('保存失败，请检查JSON格式');
    }
  };

  const columns: ColumnsType<SourceConfig> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      ellipsis: true,
    },
    {
      title: '类型',
      dataIndex: 'scraper_type',
      key: 'scraper_type',
      width: 100,
      render: (type: string) => <Tag color={type === 'http' ? 'blue' : 'green'}>{type}</Tag>,
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (active: boolean) =>
        active ? <Tag color="success">启用</Tag> : <Tag color="default">禁用</Tag>,
    },
    {
      title: '最后运行',
      dataIndex: 'last_run_at',
      key: 'last_run_at',
      width: 180,
      render: (date: string) => (date ? dayjs(date).format('YYYY-MM-DD HH:mm') : '-'),
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record: SourceConfig) => (
        <Space>
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button
            type="link"
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
            新建数据源
          </Button>
        </Card>

        <Table
          columns={columns}
          dataSource={sources}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 20 }}
        />
      </Space>

      <Modal
        title={editingSource ? '编辑数据源' : '新建数据源'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        width={800}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            label="名称"
            name="name"
            rules={[{ required: true, message: '请输入名称' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="URL"
            name="url"
            rules={[{ required: true, message: '请输入URL' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="类型"
            name="scraper_type"
            rules={[{ required: true }]}
            initialValue="http"
          >
            <Select>
              <Select.Option value="http">HTTP</Select.Option>
              <Select.Option value="browser">Browser</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="采集配置 (JSON)"
            name="config"
            rules={[{ required: true, message: '请输入配置' }]}
            extra="包含 list_selector, title_selector, url_selector, content_selector 等"
          >
            <TextArea rows={8} placeholder='{"list_selector": "ul.items > li", ...}' />
          </Form.Item>

          <Form.Item
            label="过滤规则 (JSON, 可选)"
            name="filter_rules"
            extra="包含 include_keywords, exclude_keywords, min_budget, max_budget 等"
          >
            <TextArea rows={6} placeholder='{"include_keywords": ["关键词"], ...}' />
          </Form.Item>

          <Form.Item label="定时任务 (Cron)" name="schedule_cron">
            <Input placeholder="0 0 * * *" />
          </Form.Item>

          <Form.Item
            label="启用"
            name="is_active"
            valuePropName="checked"
            initialValue={true}
          >
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </DashboardLayout>
  );
}
