'use client';

import { usePathname, useRouter } from 'next/navigation';
import { Layout, Menu, theme } from 'antd';
import {
  FileTextOutlined,
  DatabaseOutlined,
  PlayCircleOutlined,
  SettingOutlined,
} from '@ant-design/icons';

const { Header, Content, Sider } = Layout;

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const menuItems = [
    {
      key: '/tenders',
      icon: <FileTextOutlined />,
      label: '招标信息',
    },
    {
      key: '/sources',
      icon: <DatabaseOutlined />,
      label: '数据源管理',
    },
    {
      key: '/tasks',
      icon: <PlayCircleOutlined />,
      label: '任务执行',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
  ];

  const handleMenuClick = (e: { key: string }) => {
    router.push(e.key);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center', background: colorBgContainer }}>
        <div style={{ fontSize: '20px', fontWeight: 'bold', marginRight: '50px' }}>
          招标信息管理系统
        </div>
      </Header>
      <Layout>
        <Sider width={200} style={{ background: colorBgContainer }}>
          <Menu
            mode="inline"
            selectedKeys={[pathname]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
            onClick={handleMenuClick}
          />
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}
