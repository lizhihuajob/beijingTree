# 快速部署指南

## 一键启动

```bash
docker-compose up -d --build
```

## 验证部署

### 1. 检查容器状态
```bash
docker-compose ps
```

所有容器状态应该是 `Up`。

### 2. 查看后端日志
```bash
docker-compose logs -f backend
```

你应该能看到类似这样的日志：
```
开始初始化数据库...
数据库URI: postgresql://plants_user:plants_password@db:5432/plants_db
数据库连接失败，3秒后重试... (尝试 1/5)
数据库表创建完成
找到数据文件: /app/data/plants_with_real_images.json
读取到 300 条植物数据
成功初始化数据库，导入 300 条植物数据
```

### 3. 测试 API
```bash
# 健康检查
curl http://localhost/api/health

# 获取统计信息
curl http://localhost/api/statistics

# 获取植物列表
curl http://localhost/api/plants?per_page=5
```

### 4. 访问前端
打开浏览器访问：http://localhost

## 常见问题

### 问题1：页面显示植物数量为0

**原因**：数据库初始化失败或数据未正确导入。

**解决方法**：
1. 查看后端日志确认数据导入情况
2. 检查数据文件是否存在
3. 手动重新初始化数据库：
   ```bash
   docker-compose exec backend python scripts/init_db.py
   ```

### 问题2：后端无法连接数据库

**原因**：PostgreSQL 未完全就绪或网络问题。

**解决方法**：
脚本已包含自动重试机制（5次重试，每次间隔3秒）。如果还是失败：
```bash
# 重启服务
docker-compose restart backend
```

### 问题3：数据文件找不到

**原因**：Docker 卷挂载不正确。

**解决方法**：
1. 确认 `docker-compose.yml` 中的 volumes 配置正确
2. 手动挂载验证：
   ```bash
   docker-compose exec backend ls -la /app/data/
   ```

### 问题4：前端无法访问后端 API

**原因**：Nginx 反向代理配置问题。

**解决方法**：
```bash
# 查看 Nginx 日志
docker-compose logs nginx

# 重启 Nginx
docker-compose restart nginx
```

## 开发模式启动

如果需要进行开发调试，可以按以下方式启动：

### 后端（本地运行）
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
python run.py
```

### 前端（本地运行）
```bash
cd frontend
npm install
npm run dev
```

## 数据管理

### 重新初始化数据库
```bash
# 删除数据库卷（警告：会丢失所有数据）
docker-compose down -v
docker-compose up -d --build
```

### 更新爬虫数据
将新的 JSON 文件放入 `data/` 目录，然后重启后端：
```bash
docker-compose restart backend
```

### 手动触发数据同步
```bash
docker-compose exec backend python scripts/init_db.py
```

## 性能调优

### PostgreSQL 配置
编辑 `docker-compose.yml` 可以调整数据库配置：
```yaml
db:
  environment:
    POSTGRES_MAX_CONNECTIONS: 100
    POSTGRES_SHARED_BUFFERS: 256MB
```

### 后端配置
创建 `backend/.env` 文件：
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
ENABLE_SCHEDULER=true
```
