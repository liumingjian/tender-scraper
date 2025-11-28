'use client';

import { useState } from 'react';
import {
  Table,
  Input,
  Button,
  Space,
  Tag,
  Drawer,
  Form,
  InputNumber,
  message,
  Card,
  Row,
  Col,
  Typography,
  Divider,
  Select,
  DatePicker,
} from 'antd';
import {
  SearchOutlined,
  EyeOutlined,
  EditOutlined,
  ReloadOutlined,
  FilterOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import dayjs from 'dayjs';
import ReactMarkdown from 'react-markdown';
import DashboardLayout from '@/components/DashboardLayout';
import { useTenders } from '@/hooks/use-api';
import { tenderApi } from '@/lib/api';
import type { Tender, TenderUpdate, TenderFilters } from '@/types/api';

const { Text, Title, Paragraph } = Typography;
const { TextArea } = Input;
const { RangePicker } = DatePicker;

export default function TendersPage() {
  const [filters, setFilters] = useState<TenderFilters>({
    skip: 0,
    limit: 20,
    include_filtered: false,
  });
  const [selectedTender, setSelectedTender] = useState<Tender | null>(null);
  const [detailVisible, setDetailVisible] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [form] = Form.useForm();

  const { tenders, isLoading, mutate } = useTenders(filters);

  const handleSearch = (values: any) => {
    setFilters({
      ...filters,
      keyword: values.keyword || undefined,
      source_name: values.source_name || undefined,
      min_budget: values.min_budget || undefined,
      max_budget: values.max_budget || undefined,
      skip: 0,
    });
  };

  const handleViewDetail = (record: Tender) => {
    setSelectedTender(record);
    setDetailVisible(true);
    setEditMode(false);
    form.setFieldsValue({
      project_name: record.project_name,
      budget_amount: record.budget_amount,
      budget_currency: record.budget_currency || 'CNY',
      deadline: record.deadline ? dayjs(record.deadline) : null,
      contact_person: record.contact_person,
      contact_phone: record.contact_phone,
      contact_email: record.contact_email,
      location: record.location,
    });
  };

  const handleUpdate = async (values: any) => {
    if (!selectedTender) return;

    try {
      const update: TenderUpdate = {
        ...values,
        deadline: values.deadline?.toISOString(),
        is_manually_corrected: true,
      };

      await tenderApi.updateTender(selectedTender.id, update);
      message.success('更新成功');
      setEditMode(false);
      mutate(); // Refresh data

      // Update local state
      setSelectedTender({
        ...selectedTender,
        ...update,
        is_manually_corrected: true,
      });
    } catch (error) {
      message.error('更新失败');
    }
  };

  const columns: ColumnsType<Tender> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
      render: (text: string) => (
        <Text ellipsis={{ tooltip: text }} style={{ maxWidth: 300 }}>
          {text}
        </Text>
      ),
    },
    {
      title: '数据源',
      dataIndex: 'source_name',
      key: 'source_name',
      width: 150,
    },
    {
      title: '预算',
      dataIndex: 'budget_amount',
      key: 'budget_amount',
      width: 150,
      render: (amount: number, record: Tender) =>
        amount ? `¥${amount.toLocaleString()} ${record.budget_currency || ''}` : '-',
    },
    {
      title: '截止时间',
      dataIndex: 'deadline',
      key: 'deadline',
      width: 180,
      render: (date: string) => (date ? dayjs(date).format('YYYY-MM-DD HH:mm') : '-'),
    },
    {
      title: '状态',
      key: 'status',
      width: 120,
      render: (_, record: Tender) => (
        <Space direction="vertical" size={0}>
          {record.is_filtered && <Tag color="red">已过滤</Tag>}
          {record.is_manually_corrected && <Tag color="blue">已修正</Tag>}
          {!record.is_filtered && !record.is_manually_corrected && <Tag color="green">正常</Tag>}
        </Space>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record: Tender) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewDetail(record)}
          >
            查看
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <DashboardLayout>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card>
          <Form layout="inline" onFinish={handleSearch}>
            <Form.Item name="keyword">
              <Input
                placeholder="搜索关键词"
                prefix={<SearchOutlined />}
                style={{ width: 200 }}
              />
            </Form.Item>
            <Form.Item name="source_name">
              <Input placeholder="数据源" style={{ width: 150 }} />
            </Form.Item>
            <Form.Item name="min_budget">
              <InputNumber placeholder="最小预算" style={{ width: 120 }} min={0} />
            </Form.Item>
            <Form.Item name="max_budget">
              <InputNumber placeholder="最大预算" style={{ width: 120 }} min={0} />
            </Form.Item>
            <Form.Item>
              <Space>
                <Button type="primary" htmlType="submit" icon={<FilterOutlined />}>
                  筛选
                </Button>
                <Button
                  icon={<ReloadOutlined />}
                  onClick={() => {
                    setFilters({ skip: 0, limit: 20, include_filtered: false });
                    mutate();
                  }}
                >
                  重置
                </Button>
              </Space>
            </Form.Item>
          </Form>
        </Card>

        <Table
          columns={columns}
          dataSource={tenders}
          rowKey="id"
          loading={isLoading}
          pagination={{
            current: (filters.skip || 0) / (filters.limit || 20) + 1,
            pageSize: filters.limit || 20,
            total: (tenders?.length || 0) + (filters.skip || 0),
            onChange: (page, pageSize) => {
              setFilters({
                ...filters,
                skip: (page - 1) * pageSize,
                limit: pageSize,
              });
            },
          }}
        />
      </Space>

      <Drawer
        title={
          <Space>
            <span>招标详情</span>
            {selectedTender?.is_manually_corrected && <Tag color="blue">已修正</Tag>}
          </Space>
        }
        placement="right"
        width={720}
        onClose={() => setDetailVisible(false)}
        open={detailVisible}
        extra={
          <Space>
            {!editMode ? (
              <Button type="primary" icon={<EditOutlined />} onClick={() => setEditMode(true)}>
                编辑
              </Button>
            ) : (
              <>
                <Button onClick={() => setEditMode(false)}>取消</Button>
                <Button type="primary" onClick={() => form.submit()}>
                  保存
                </Button>
              </>
            )}
          </Space>
        }
      >
        {selectedTender && (
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <Card title="基本信息" size="small">
              <Row gutter={[16, 16]}>
                <Col span={24}>
                  <Text strong>标题：</Text>
                  <Paragraph>{selectedTender.title}</Paragraph>
                </Col>
                <Col span={12}>
                  <Text strong>数据源：</Text>
                  <Text>{selectedTender.source_name}</Text>
                </Col>
                <Col span={12}>
                  <Text strong>发布时间：</Text>
                  <Text>
                    {selectedTender.published_at
                      ? dayjs(selectedTender.published_at).format('YYYY-MM-DD HH:mm')
                      : '-'}
                  </Text>
                </Col>
                <Col span={24}>
                  <Text strong>原文链接：</Text>
                  <br />
                  <a href={selectedTender.source_url} target="_blank" rel="noopener noreferrer">
                    {selectedTender.source_url}
                  </a>
                </Col>
              </Row>
            </Card>

            <Divider />

            {editMode ? (
              <Card title="提取信息（编辑模式）" size="small">
                <Form form={form} layout="vertical" onFinish={handleUpdate}>
                  <Form.Item label="项目名称" name="project_name">
                    <Input />
                  </Form.Item>
                  <Row gutter={16}>
                    <Col span={16}>
                      <Form.Item label="预算金额" name="budget_amount">
                        <InputNumber style={{ width: '100%' }} min={0} />
                      </Form.Item>
                    </Col>
                    <Col span={8}>
                      <Form.Item label="货币" name="budget_currency">
                        <Select>
                          <Select.Option value="CNY">CNY</Select.Option>
                          <Select.Option value="USD">USD</Select.Option>
                          <Select.Option value="EUR">EUR</Select.Option>
                        </Select>
                      </Form.Item>
                    </Col>
                  </Row>
                  <Form.Item label="截止时间" name="deadline">
                    <DatePicker showTime style={{ width: '100%' }} />
                  </Form.Item>
                  <Form.Item label="联系人" name="contact_person">
                    <Input />
                  </Form.Item>
                  <Form.Item label="联系电话" name="contact_phone">
                    <Input />
                  </Form.Item>
                  <Form.Item label="联系邮箱" name="contact_email">
                    <Input type="email" />
                  </Form.Item>
                  <Form.Item label="项目地点" name="location">
                    <Input />
                  </Form.Item>
                </Form>
              </Card>
            ) : (
              <Card title="提取信息" size="small">
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Text strong>项目名称：</Text>
                    <Text>{selectedTender.project_name || '-'}</Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>预算：</Text>
                    <Text>
                      {selectedTender.budget_amount
                        ? `¥${selectedTender.budget_amount.toLocaleString()} ${
                            selectedTender.budget_currency || ''
                          }`
                        : '-'}
                    </Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>截止时间：</Text>
                    <Text>
                      {selectedTender.deadline
                        ? dayjs(selectedTender.deadline).format('YYYY-MM-DD HH:mm')
                        : '-'}
                    </Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>联系人：</Text>
                    <Text>{selectedTender.contact_person || '-'}</Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>联系电话：</Text>
                    <Text>{selectedTender.contact_phone || '-'}</Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>联系邮箱：</Text>
                    <Text>{selectedTender.contact_email || '-'}</Text>
                  </Col>
                  <Col span={12}>
                    <Text strong>项目地点：</Text>
                    <Text>{selectedTender.location || '-'}</Text>
                  </Col>
                </Row>
              </Card>
            )}

            <Divider />

            <Card title="正文内容" size="small">
              <div
                style={{
                  maxHeight: '400px',
                  overflow: 'auto',
                  padding: '12px',
                  background: '#f5f5f5',
                  borderRadius: '4px',
                }}
              >
                <ReactMarkdown>{selectedTender.content}</ReactMarkdown>
              </div>
            </Card>

            {selectedTender.is_filtered && (
              <Card title="过滤信息" size="small">
                <Text type="danger">过滤原因：{selectedTender.filter_reason}</Text>
              </Card>
            )}
          </Space>
        )}
      </Drawer>
    </DashboardLayout>
  );
}
