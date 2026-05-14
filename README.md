# 北京植物园植物数据库

一个展示北京植物园植物信息的全栈 Web 应用，包含独立的管理后台系统。

## 功能特性

### 主站功能
- 📚 浏览所有植物信息
- 🔍 按名称、科属、描述搜索植物
- 🏷️ 按科属或园区筛选植物
- 🏛️ 珍稀保护植物展示
- 📱 响应式设计，支持移动端

### 管理后台功能
- 🔐 管理员登录认证
- 👤 个人中心（修改密码、系统信息）
- 📊 数据仪表盘（植物统计、访问统计）
- 🌿 植物CRUD管理（添加、编辑、删除）
- 🔧 爬虫配置管理（执行频率、开关控制）
- 🍎 苹果设计风格的UI界面

## 技术栈

- **前端**: React + Vite + Tailwind CSS
- **管理前端**: React + 独立入口
- **后端**: Flask + SQLAlchemy
- **管理后端**: Flask + JWT认证
- **数据库**: PostgreSQL
- **部署**: Docker + Nginx

## 端口说明

| 服务 | 端口 | 地址 | 说明 |
|------|------|------|------|
| 主站前端 | 80 | http://localhost | 北京植物园植物数据库 |
| 管理后台 | 8080 | http://localhost:8080 | 独立管理系统 |
| 主站API | 5000 | - | Nginx代理到 /api |
| 管理API | 5001 | - | Nginx代理到 /admin/api |

## 快速开始

### 使用 Docker 部署（推荐）

1. 确保已安装 Docker 和 Docker Compose

2. 克隆项目并进入目录

3. 启动所有服务：
   ```bash
   docker compose up -d --build
   ```

4. 访问应用：
   - 主站: http://localhost
   - 管理后台: http://localhost:8080
   - 默认管理员账号: admin / admin

5. 停止服务：
   ```bash
   docker compose down
   ```

### 本地开发

#### 主站后端

1. 进入后端目录：
   ```bash
   cd backend
   ```

2. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. 初始化数据库：
   ```bash
   python scripts/init_db.py
   ```

4. 启动后端服务（端口5000）：
   ```bash
   python run.py
   ```

#### 管理后端

1. 初始化管理员账号：
   ```bash
   python scripts/init_admin.py
   ```

2. 启动管理后端服务（端口5001）：
   ```bash
   python -m flask run --port 5001
   ```

#### 主站前端

1. 进入前端目录：
   ```bash
   cd frontend
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动开发服务器：
   ```bash
   npm run dev
   ```

#### 管理前端

1. 启动管理前端开发服务器：
   ```bash
   npm run dev:admin
   ```

## API 文档

### 获取所有植物
```
GET /api/plants
```

查询参数：
- `page`: 页码（默认: 1）
- `per_page`: 每页数量（默认: 50）
- `search`: 搜索关键词
- `family`: 按科属筛选
- `zone`: 按园区筛选

### 获取单个植物
```
GET /api/plants/:id
```

### 获取统计信息
```
GET /api/statistics
```

### 获取所有科属
```
GET /api/families
```

### 获取所有园区
```
GET /api/zones
```

### 获取保护植物
```
GET /api/protected
```

## 项目结构

```
beijingTree/
├── backend/                 # 后端服务
│   ├── admin_app/          # 管理后台应用
│   │   ├── __init__.py
│   │   └── routes.py       # 管理API路由
│   ├── app/                # Flask 应用
│   │   ├── __init__.py
│   │   ├── models.py       # 数据模型（含Admin、SpiderConfig、VisitLog）
│   │   ├── routes.py       # 主站API路由
│   │   └── scheduler.py    # 定时任务
│   ├── config/             # 配置文件
│   ├── scripts/            # 脚本文件
│   │   ├── init_db.py
│   │   └── init_admin.py
│   ├── Dockerfile
│   ├── Dockerfile.admin
│   └── requirements.txt
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── admin/          # 管理前端
│   │   │   ├── pages/      # 管理页面
│   │   │   ├── components/ # 管理组件
│   │   │   └── services/   # 管理API服务
│   │   ├── pages/          # 主站页面
│   │   ├── components/     # 通用组件
│   │   ├── services/       # API服务
│   │   └── utils/          # 工具函数
│   ├── index.html          # 主站入口
│   ├── index-admin.html    # 管理前端入口
│   ├── vite.config.js      # 主站构建配置
│   ├── vite.config.admin.js # 管理前端构建配置
│   ├── Dockerfile
│   ├── Dockerfile.admin
│   ├── nginx-admin.conf
│   └── package.json
├── nginx/                  # Nginx 配置
│   └── nginx.conf
├── data/                   # 数据文件
└── docker-compose.yml
```

## 管理后台API文档

### 认证
```
POST /admin/api/auth/login  # 登录
GET  /admin/api/auth/me     # 获取当前用户
POST /admin/api/auth/change-password  # 修改密码
```

### 仪表盘
```
GET /admin/api/dashboard/stats     # 获取统计数据
GET /admin/api/dashboard/visit-trend  # 获取访问趋势
```

### 植物管理
```
GET    /admin/api/plants         # 获取植物列表
GET    /admin/api/plants/:id     # 获取单个植物
POST   /admin/api/plants         # 创建植物
PUT    /admin/api/plants/:id     # 更新植物
DELETE /admin/api/plants/:id     # 删除植物
```

### 爬虫配置
```
GET  /admin/api/spider/config  # 获取配置
PUT  /admin/api/spider/config  # 更新配置
POST /admin/api/spider/run-now # 立即执行
```

### 系统信息
```
GET /admin/api/system/info   # 获取系统信息
GET /admin/api/health        # 健康检查
```

## 定时任务

应用包含定时任务，每天凌晨 2 点自动更新植物数据。可以通过环境变量 `ENABLE_SCHEDULER` 控制是否启用。

## 环境变量

### 后端

- `FLASK_ENV`: 运行环境 (development/production)
- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: Flask 密钥
- `ENABLE_SCHEDULER`: 是否启用定时任务 (true/false)
- `CORS_ORIGINS`: 允许的跨域来源

### 前端

- `VITE_API_URL`: API 地址

## 许可证

MIT

