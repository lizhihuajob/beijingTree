# 北京植物园植物数据库

一个展示北京植物园植物信息的全栈 Web 应用。

## 功能特性

- 📚 浏览所有植物信息
- 🔍 按名称、科属、描述搜索植物
- 🏷️ 按科属或园区筛选植物
- 🏛️ 珍稀保护植物展示
- 📱 响应式设计，支持移动端

## 技术栈

- **前端**: React + Vite + Tailwind CSS
- **后端**: Flask + SQLAlchemy
- **数据库**: PostgreSQL
- **部署**: Docker + Nginx

## 快速开始

### 使用 Docker 部署（推荐）

1. 确保已安装 Docker 和 Docker Compose

2. 克隆项目并进入目录

3. 启动所有服务：
   ```bash
   docker-compose up -d --build
   ```

4. 访问应用：
   - 前端: http://localhost
   - API: http://localhost/api

5. 停止服务：
   ```bash
   docker-compose down
   ```

### 本地开发

#### 后端

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

4. 启动后端服务：
   ```bash
   python run.py
   ```

#### 前端

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
│   ├── app/                # Flask 应用
│   │   ├── __init__.py
│   │   ├── models.py       # 数据模型
│   │   ├── routes.py       # API 路由
│   │   └── scheduler.py    # 定时任务
│   ├── config/             # 配置文件
│   ├── scripts/            # 脚本文件
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── pages/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── services/      # API 服务
│   │   └── utils/         # 工具函数
│   ├── Dockerfile
│   └── nginx.conf
├── nginx/                  # Nginx 配置
├── data/                   # 数据文件
└── docker-compose.yml
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

