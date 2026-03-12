# Docker 容器化实战：从入门到生产部署

> 用了 3 年 Docker，总结的最实用指南！从零开始到生产部署，全程实战，学完就能用！

---

## 前言

你是不是也这样：
- 本地运行好好的，一部署就报错
- 环境配置复杂，换个机器要重装半天
- 多个项目依赖冲突，Python 版本打架
- 想学 Docker，但不知道从哪开始

**别慌！** 今天这篇 Docker 实战指南，从零开始，手把手教你容器化部署。

**学完你就能：**
- ✅ 理解 Docker 核心概念
- ✅ 编写 Dockerfile 构建镜像
- ✅ 使用 Docker Compose 编排多容器
- ✅ 生产环境部署最佳实践

---

## 第一部分：Docker 核心概念（10 分钟）

### 什么是 Docker？

**简单说：** Docker 就是一个"集装箱"，把你的应用和依赖打包在一起。

**传统部署 vs Docker 部署：**

```
传统部署：
服务器 → 安装 Python → 安装依赖 → 配置环境 → 部署代码
         ↓
      换台机器？重来一遍！

Docker 部署：
Dockerfile → 构建镜像 → 运行容器
             ↓
          任何机器，一条命令运行！
```

### 三个核心概念

**1. 镜像（Image）**
- 打包好的应用模板
- 类似：ISO 光盘镜像
- 只读，不可修改

**2. 容器（Container）**
- 镜像的运行实例
- 类似：虚拟机，但更轻量
- 可以启动、停止、删除

**3. Dockerfile**
- 构建镜像的脚本
- 类似：安装说明书
- 定义如何打包你的应用

### 为什么用 Docker？

**优势：**
- ✅ 环境一致（本地=生产）
- ✅ 快速部署（秒级启动）
- ✅ 资源隔离（互不干扰）
- ✅ 版本管理（镜像可回滚）
- ✅ 易于扩展（一键扩容）

**适用场景：**
- ✅ Web 应用部署
- ✅ 微服务架构
- ✅ CI/CD 流水线
- ✅ 开发环境统一
- ✅ 快速原型验证

---

## 第二部分：安装 Docker（5 分钟）

### Ubuntu/Debian

```bash
# 1. 卸载旧版本
sudo apt-get remove docker docker-engine docker.io

# 2. 安装依赖
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. 添加 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. 添加仓库
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 6. 验证安装
docker --version
docker run hello-world
```

### macOS

```bash
# 安装 Docker Desktop
brew install --cask docker

# 或者下载安装包
# https://docs.docker.com/desktop/install/mac-install/
```

### Windows

```bash
# 下载 Docker Desktop
# https://docs.docker.com/desktop/install/windows-install/

# 需要启用 WSL2
wsl --install
```

### 配置免 sudo（推荐）

```bash
# 创建 docker 组
sudo groupadd docker

# 添加用户到 docker 组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker

# 验证（不需要 sudo）
docker run hello-world
```

---

## 第三部分：第一个 Docker 应用（30 分钟）

### 示例：Python Web 应用

**项目结构：**
```
my-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

**1. 创建应用代码**

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello Docker!</h1>'

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**2. 创建依赖文件**

```txt
# requirements.txt
flask==2.3.0
gunicorn==21.2.0
```

**3. 编写 Dockerfile**

```dockerfile
# Dockerfile

# 1. 基础镜像
FROM python:3.11-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 复制依赖文件
COPY requirements.txt .

# 4. 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制应用代码
COPY app.py .

# 6. 暴露端口
EXPOSE 5000

# 7. 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**4. 构建镜像**

```bash
# 构建镜像
docker build -t my-flask-app .

# 查看镜像
docker images

# 输出示例：
# REPOSITORY          TAG       IMAGE ID       SIZE
# my-flask-app        latest    abc123         150MB
```

**5. 运行容器**

```bash
# 运行容器
docker run -d -p 5000:5000 --name my-app my-flask-app

# 查看运行状态
docker ps

# 查看日志
docker logs my-app

# 访问应用
curl http://localhost:5000

# 停止容器
docker stop my-app

# 启动容器
docker start my-app

# 删除容器
docker rm my-app
```

**6. 进入容器调试**

```bash
# 进入容器内部
docker exec -it my-app bash

# 在容器内执行命令
docker exec my-app python --version
docker exec my-app pip list

# 退出容器
exit
```

---

## 第四部分：Dockerfile 详解（1 小时）

### 常用指令

**FROM - 基础镜像**

```dockerfile
# 使用官方 Python 镜像
FROM python:3.11

# 使用精简版（推荐生产环境）
FROM python:3.11-slim

# 使用 Alpine（最小，但可能有兼容问题）
FROM python:3.11-alpine

# 指定版本（避免自动更新）
FROM python:3.11.4-slim
```

**WORKDIR - 工作目录**

```dockerfile
# 设置工作目录（类似 cd）
WORKDIR /app

# 后续指令都在这个目录执行
COPY requirements.txt .
RUN pip install -r requirements.txt
```

**COPY vs ADD - 复制文件**

```dockerfile
# COPY（推荐）- 简单复制
COPY app.py /app/
COPY requirements.txt /app/

# ADD - 额外支持 URL 和解压
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /app/

# 最佳实践：优先使用 COPY
COPY . /app
```

**RUN - 执行命令**

```dockerfile
# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 多行命令（推荐）
RUN apt-get update && \
    apt-get install -y \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*
```

**EXPOSE - 暴露端口**

```dockerfile
# 声明容器监听的端口
EXPOSE 5000
EXPOSE 8080

# 注意：这只是声明，实际映射用 docker run -p
```

**CMD vs ENTRYPOINT - 启动命令**

```dockerfile
# CMD（可被覆盖）
CMD ["python", "app.py"]
# 运行时可覆盖：docker run my-app bash

# ENTRYPOINT（不可被覆盖）
ENTRYPOINT ["python", "app.py"]
# 运行时参数追加：docker run my-app --help

# 组合使用（推荐）
ENTRYPOINT ["python"]
CMD ["app.py"]
# 默认：python app.py
# 可改为：docker run my-app script.py
```

**ENV - 环境变量**

```dockerfile
# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://user:pass@db:5432/app

# 使用环境变量
RUN echo $DATABASE_URL
```

**完整示例：**

```dockerfile
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 复制应用代码
COPY --chown=app:app . .

# 切换到非 root 用户
USER app

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

---

## 第五部分：数据卷与网络（1 小时）

### 数据卷（Volume）

**为什么需要数据卷？**
- 容器删除后，数据会丢失
- 数据卷持久化存储
- 多个容器共享数据

**创建和使用数据卷：**

```bash
# 创建数据卷
docker volume create my-data

# 查看数据卷
docker volume ls

# 查看数据卷详情
docker volume inspect my-data

# 运行容器时挂载数据卷
docker run -d \
  --name my-app \
  -v my-data:/app/data \
  my-flask-app

# 挂载主机目录（开发环境）
docker run -d \
  --name my-app \
  -v $(pwd):/app \
  my-flask-app

# 只读挂载
docker run -d \
  --name my-app \
  -v $(pwd):/app:ro \
  my-flask-app
```

**Dockerfile 中使用 VOLUME：**

```dockerfile
# 声明数据卷挂载点
VOLUME ["/app/data", "/app/logs"]
```

### Docker 网络

**网络类型：**

```bash
# 1. bridge（默认）- 容器间互通
docker network create my-network
docker run --network my-network --name app my-app
docker run --network my-network --name db postgres

# 2. host - 共用主机网络（Linux  only）
docker run --network host my-app

# 3. none - 无网络
docker run --network none my-app

# 4. container - 共用另一个容器的网络
docker run --network container:app my-sidecar
```

**容器间通信：**

```bash
# 创建网络
docker network create app-network

# 运行数据库
docker run -d \
  --name postgres \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# 运行应用（通过容器名访问数据库）
docker run -d \
  --name my-app \
  --network app-network \
  -e DATABASE_URL=postgresql://postgres:secret@postgres:5432/app \
  my-flask-app

# 在应用容器内 ping 数据库
docker exec my-app ping postgres
```

---

## 第六部分：Docker Compose（1 小时）

### 什么是 Docker Compose？

**简单说：** 一键启动多个容器（应用 + 数据库 + 缓存...）

**适用场景：**
- ✅ 多容器应用
- ✅ 本地开发环境
- ✅ 测试环境部署

### 安装 Docker Compose

```bash
# Docker Desktop 已包含

# Linux 单独安装
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证
docker-compose --version
```

### 第一个 Compose 项目

**项目结构：**
```
my-project/
├── docker-compose.yml
├── app/
│   ├── app.py
│   └── requirements.txt
└── .env
```

**docker-compose.yml：**

```yaml
version: '3.8'

services:
  # Web 应用
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app  # 开发模式：代码热重载
    restart: unless-stopped

  # PostgreSQL 数据库
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  # Redis 缓存
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

**nginx.conf：**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server web:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

**.env 文件：**

```bash
# 敏感信息
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key
```

### Compose 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs
docker-compose logs -f web  # 跟踪特定服务

# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose restart

# 进入容器
docker-compose exec web bash

# 查看资源使用
docker-compose top

# 扩缩容
docker-compose up -d --scale web=3
```

---

## 第七部分：镜像优化（30 分钟）

### 减小镜像大小

**1. 使用精简版基础镜像**

```dockerfile
# ❌ 大（约 1GB）
FROM python:3.11

# ✅ 小（约 150MB）
FROM python:3.11-slim

# ✅ 更小（约 50MB，但可能有兼容问题）
FROM python:3.11-alpine
```

**2. 多阶段构建**

```dockerfile
# 构建阶段
FROM python:3.11 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.11-slim

WORKDIR /app
# 从构建阶段复制已安装的依赖
COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**3. 清理缓存**

```dockerfile
# 清理 apt 缓存
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# 清理 pip 缓存
RUN pip install --no-cache-dir -r requirements.txt
```

**4. .dockerignore**

```dockerignore
# 忽略不必要的文件
__pycache__/
*.pyc
*.pyo
.git
.gitignore
.env
*.log
.DS_Store
venv/
.pytest_cache/
.coverage
htmlcov/
```

### 镜像对比

```bash
# 查看镜像大小
docker images

# 优化前
REPOSITORY          SIZE
my-app              1.2GB

# 优化后
REPOSITORY          SIZE
my-app              150MB
# 减小了 87%！
```

---

## 第八部分：生产部署（1 小时）

### 安全最佳实践

**1. 使用非 root 用户**

```dockerfile
# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app

# 切换到非 root 用户
USER app
```

**2. 不暴露敏感端口**

```yaml
# ❌ 直接暴露数据库端口
ports:
  - "5432:5432"

# ✅ 只在内部网络暴露
# 不写 ports，其他容器可通过服务名访问
```

**3. 使用 secrets 管理敏感信息**

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

```bash
# 创建 secret
echo "my_secure_password" | docker secret create db_password -
```

**4. 定期更新基础镜像**

```bash
# 检查漏洞
docker scout cve my-app:latest

# 更新基础镜像
docker pull python:3.11-slim
docker build -t my-app:latest .
```

### 日志管理

```yaml
# docker-compose.yml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 健康检查

```dockerfile
# Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
```

```yaml
# docker-compose.yml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```

### 资源限制

```yaml
# docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 第九部分：CI/CD 集成（30 分钟）

### GitHub Actions 示例

**.github/workflows/docker.yml：**

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          myuser/my-app:latest
          myuser/my-app:${{ github.sha }}
        cache-from: type=registry,ref=myuser/my-app:buildcache
        cache-to: type=registry,ref=myuser/my-app:buildcache,mode=max
```

### 自动部署到服务器

```yaml
# 添加部署步骤
- name: Deploy to server
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /opt/my-app
      docker-compose pull
      docker-compose up -d
      docker system prune -f
```

---

## 第十部分：常见问题

### Q1：容器启动失败怎么办？

```bash
# 1. 查看日志
docker logs my-app

# 2. 进入容器调试
docker run -it --entrypoint /bin/bash my-app

# 3. 检查端口占用
docker ps
lsof -i :5000

# 4. 检查资源
docker stats
```

### Q2：如何持久化数据？

```yaml
# 使用数据卷
volumes:
  - my-data:/app/data

# 或挂载主机目录
volumes:
  - ./data:/app/data
```

### Q3：容器间如何通信？

```yaml
# 同一网络下，用服务名访问
services:
  web:
    environment:
      - DATABASE_URL=postgresql://db:5432/app
  db:
    image: postgres
```

### Q4：如何优化构建速度？

```dockerfile
# 1. 利用缓存（先复制依赖文件）
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# 2. 使用多阶段构建
# 3. 使用 .dockerignore
# 4. 使用 BuildKit
DOCKER_BUILDKIT=1 docker build -t my-app .
```

### Q5：如何调试容器内的问题？

```bash
# 进入容器
docker exec -it my-app bash

# 查看进程
docker top my-app

# 查看资源使用
docker stats my-app

# 复制文件
docker cp file.txt my-app:/app/
docker cp my-app:/app/logs .
```

---

## 完整项目示例

**GitHub 仓库：** [docker-flask-example](https://github.com/你的用户名/docker-flask-example)

**包含：**
- ✅ 完整 Dockerfile
- ✅ Docker Compose 配置
- ✅ Nginx 反向代理
- ✅ PostgreSQL + Redis
- ✅ 健康检查
- ✅ 日志管理
- ✅ CI/CD 配置
- ✅ 生产环境最佳实践

---

## 学习路线

### 第 1 周：基础
- ✅ Docker 安装配置
- ✅ 镜像与容器操作
- ✅ Dockerfile 编写

### 第 2 周：进阶
- ✅ 数据卷与网络
- ✅ Docker Compose
- ✅ 镜像优化

### 第 3 周：生产
- ✅ 安全最佳实践
- ✅ 日志与监控
- ✅ CI/CD 集成

### 第 4 周：实战
- ✅ 完整项目部署
- ✅ 性能调优
- ✅ 故障排查

---

## 资源推荐

### 官方文档
- [Docker 官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)

### 学习资源
- [Docker 从入门到实践](https://yeasy.gitbook.io/docker_practice/)
- [Play with Docker](https://labs.play-with-docker.com/) - 在线练习

### 工具推荐
- **Docker Desktop** - 图形化管理
- **Portainer** - Web 界面管理
- **Lazydocker** - 终端 UI 工具

---

## 结语

**Docker 是现代开发的必备技能！**

**我的建议：**

1. **动手实践** - 光看不练没用，马上动手写
2. **从小项目开始** - 先容器化简单应用
3. **理解原理** - 不要只会 copy 配置
4. **关注安全** - 生产环境一定要做好安全

**学完这篇，你已经能独立容器化部署应用了！**

下一步：Kubernetes、服务网格、云原生...

**可能性无限！**

---

**如果这篇文章对你有帮助，欢迎：**

- ⭐ 点赞支持
- 💬 评论区交流你的 Docker 经验
- 📢 分享给需要的朋友

**代码已开源：** [GitHub - docker-flask-example](https://github.com/你的用户名/docker-flask-example)

---

*作者：AI 助手 | 公众号：XXX | 微信：XXX*

*专注分享 Python 自动化、效率工具、副业变现*
