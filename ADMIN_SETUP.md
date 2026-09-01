# 管理后台使用说明

## 后端启动

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库和管理员账号
```bash
# 初始化主数据库
python scripts/init_db.py

# 初始化管理员账号
python scripts/init_admin.py
```

默认管理员账号：
- 用户名：admin
- 密码：admin

### 3. 启动管理后台服务
```bash
# 启动管理后台（端口 5001）
python run_admin.py
```

### 4. 启动主API服务（端口 5000）
```bash
python run.py
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

## 访问地址

- 主站：http://localhost:5173
- 管理后台：http://localhost:5173/admin
- 管理API：http://localhost:5001/admin/api

## 功能说明

### 1. 仪表盘
- 显示植物总数、科属数量、受保护植物数量
- 显示访问统计（今日访问、本周访问、总访问量）
- 访问趋势图表

### 2. 植物管理
- 查看植物列表
- 搜索植物
- 编辑植物信息
- 删除植物
- 添加新植物

### 3. 爬虫配置
- 启用/禁用爬虫
- 配置执行频率（每日固定时间/时间间隔）
- 立即执行爬虫

### 4. 个人中心
- 修改管理员密码
- 查看系统信息

## 端口说明

- 主API端口：5000
- 管理API端口：5001
- 前端端口：5173

## 安全说明

1. 首次登录后请立即修改默认密码
2. 生产环境请修改 SECRET_KEY
3. 建议使用 HTTPS 部署

## API 端点

### 认证
- POST /admin/api/auth/login - 登录
- GET /admin/api/auth/me - 获取当前用户
- POST /admin/api/auth/change-password - 修改密码

### 植物管理
- GET /admin/api/plants - 获取植物列表
- GET /admin/api/plants/:id - 获取植物详情
- POST /admin/api/plants - 创建植物
- PUT /admin/api/plants/:id - 更新植物
- DELETE /admin/api/plants/:id - 删除植物

### 爬虫配置
- GET /admin/api/spider/config - 获取配置
- PUT /admin/api/spider/config - 更新配置
- POST /admin/api/spider/run-now - 立即执行

### 系统信息
- GET /admin/api/system/info - 系统信息
- GET /admin/api/dashboard/stats - 仪表盘统计
- GET /admin/api/dashboard/visit-trend - 访问趋势
