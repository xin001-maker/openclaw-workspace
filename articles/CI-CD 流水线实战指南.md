# CI/CD 流水线实战指南

> 从代码提交到生产部署：自动化交付的完整实践

## 📋 目录

1. [CI/CD 核心概念](#cicd-核心概念)
2. [为什么需要 CI/CD](#为什么需要-cicd)
3. [流水线设计原则](#流水线设计原则)
4. [主流工具对比](#主流工具对比)
5. [GitHub Actions 实战](#github-actions-实战)
6. [GitLab CI 实战](#gitlab-ci-实战)
7. [Jenkins 实战](#jenkins-实战)
8. [Docker + K8s 部署](#docker--k8s-部署)
9. [最佳实践](#最佳实践)
10. [故障排查](#故障排查)

---

## CI/CD 核心概念

### 术语解释

```
┌─────────────────────────────────────────────────────┐
│                    CI/CD 流水线                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CI (Continuous Integration) 持续集成               │
│  └─ 频繁合并代码 → 自动构建 → 自动测试              │
│                                                     │
│  CD (Continuous Delivery) 持续交付                  │
│  └─ 自动部署到测试/预发环境，手动批准生产           │
│                                                     │
│  CD (Continuous Deployment) 持续部署                │
│  └─ 全自动部署到生产环境（无需人工干预）             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 典型流水线流程

```
┌──────────────────────────────────────────────────────────────┐
│                     CI/CD Pipeline                           │
└──────────────────────────────────────────────────────────────┘

代码提交
   │
   ↓
┌─────────────┐
│   Code      │ 代码检查 (Lint, Format)
│   Review    │ 自动化审查
└─────────────┘
   │
   ↓
┌─────────────┐
│   Build     │ 编译构建
│             │ 依赖安装
└─────────────┘
   │
   ↓
┌─────────────┐
│    Test     │ 单元测试
│             │ 集成测试
│             │ 端到端测试
└─────────────┘
   │
   ↓
┌─────────────┐
│   Security  │ 安全扫描
│   Scan      │ 漏洞检测
└─────────────┘
   │
   ↓
┌─────────────┐
│   Docker    │ 构建镜像
│   Build     │ 推送仓库
└─────────────┘
   │
   ↓
┌─────────────┐
│  Deploy to  │ 部署到
│   Staging   │ 预发环境
└─────────────┘
   │
   ↓
┌─────────────┐
│   Manual    │ 人工审批
│   Approval  │ (可选)
└─────────────┘
   │
   ↓
┌─────────────┐
│  Deploy to  │ 部署到
│ Production  │ 生产环境
└─────────────┘
   │
   ↓
┌─────────────┐
│  Monitor &  │ 监控
│  Rollback   │ 回滚机制
└─────────────┘
```

---

## 为什么需要 CI/CD

### 传统部署的痛点

```
❌ 手动部署流程

开发人员
   │
   ├─ 1. 本地构建 (30 分钟)
   │
   ├─ 2. 上传代码到服务器 (10 分钟)
   │
   ├─ 3. SSH 登录服务器 (5 分钟)
   │
   ├─ 4. 手动执行部署脚本 (15 分钟)
   │
   ├─ 5. 重启服务 (5 分钟)
   │
   └─ 6. 手动验证功能 (30 分钟)
   
总耗时：95 分钟/次
错误率：~15%
频率：每周 1-2 次
```

### CI/CD 带来的改进

```
✅ 自动化部署流程

代码提交
   │
   ├─ 自动触发流水线 (0 分钟)
   │
   ├─ 自动构建 + 测试 (15 分钟)
   │
   ├─ 自动部署到预发 (5 分钟)
   │
   ├─ 自动化测试验证 (10 分钟)
   │
   └─ 自动/手动部署到生产 (5 分钟)
   
总耗时：35 分钟/次
错误率：< 1%
频率：每天 10+ 次
```

### 量化收益

| 指标 | 手动部署 | CI/CD | 提升 |
|------|----------|-------|------|
| 部署时间 | 95 分钟 | 35 分钟 | 63% ↓ |
| 部署频率 | 2 次/周 | 10 次/天 | 35 倍 ↑ |
| 失败率 | 15% | <1% | 93% ↓ |
| 恢复时间 | 4 小时 | 10 分钟 | 96% ↓ |
| 人力成本 | 2 人/次 | 0 人/次 | 100% ↓ |

---

## 流水线设计原则

### 1. 快速反馈

```yaml
# ❌ 错误：所有测试串行执行
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - run: npm test:unit  # 20 分钟
  
  test-integration:
    runs-on: ubuntu-latest
    needs: test-unit  # 必须等单元测试完成
    steps:
      - run: npm test:integration  # 30 分钟
  
  test-e2e:
    runs-on: ubuntu-latest
    needs: test-integration  # 必须等集成测试完成
    steps:
      - run: npm test:e2e  # 40 分钟

总耗时：90 分钟

# ✅ 正确：并行执行独立测试
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - run: npm test:unit  # 20 分钟
  
  test-integration:
    runs-on: ubuntu-latest
    steps:
      - run: npm test:integration  # 30 分钟
  
  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - run: npm test:e2e  # 40 分钟

总耗时：40 分钟 (并行)
```

### 2. 失败快速

```yaml
# ✅ 将快速检查放在前面
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint  # 1 分钟，快速失败
  
  type-check:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - run: npm run typecheck  # 2 分钟
  
  test:
    runs-on: ubuntu-latest
    needs: type-check
    steps:
      - run: npm test  # 20 分钟
```

### 3. 可重复性

```dockerfile
# ✅ 使用固定版本的基础镜像
FROM node:18.17.0-alpine

# ✅ 锁定依赖版本
COPY package.json package-lock.json ./
RUN npm ci  # 使用 lock 文件，不用 npm install

# ✅ 设置固定工作目录
WORKDIR /app

# ✅ 明确暴露端口
EXPOSE 3000

# ✅ 使用非 root 用户
USER node

CMD ["node", "dist/server.js"]
```

### 4. 幂等性

```bash
#!/bin/bash
# ✅ 幂等的部署脚本

# 检查服务是否已运行
if systemctl is-active --quiet myapp; then
    echo "服务已运行，执行滚动更新"
    systemctl reload myapp
else
    echo "服务未运行，执行全新部署"
    systemctl start myapp
fi

# 健康检查
for i in {1..10}; do
    if curl -s http://localhost:3000/health | grep -q "ok"; then
        echo "部署成功"
        exit 0
    fi
    sleep 5
done

echo "部署失败，回滚"
exit 1
```

### 5. 可观测性

```yaml
# ✅ 每个步骤都有清晰的日志
jobs:
  deploy:
    steps:
      - name: 📦 构建 Docker 镜像
        run: |
          echo "开始构建镜像..."
          echo "镜像标签：${{ github.sha }}"
          docker build -t myapp:${{ github.sha }} .
      
      - name: 🚀 推送镜像到仓库
        run: |
          echo "推送到 registry.example.com..."
          docker push registry.example.com/myapp:${{ github.sha }}
      
      - name: 🎯 部署到 Kubernetes
        run: |
          echo "更新部署..."
          kubectl set image deployment/myapp myapp=registry.example.com/myapp:${{ github.sha }}
          
      - name: ✅ 健康检查
        run: |
          echo "等待部署完成..."
          kubectl rollout status deployment/myapp
```

---

## 主流工具对比

### 工具选型矩阵

| 工具 | 类型 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| GitHub Actions | SaaS | 与 GitHub 深度集成，免费额度高 | 仅限 GitHub | GitHub 项目 |
| GitLab CI | 自托管/SaaS | 功能完整，配置灵活 | 学习曲线 | GitLab 用户 |
| Jenkins | 自托管 | 插件丰富，高度可定制 | 维护成本高 | 企业级复杂场景 |
| CircleCI | SaaS | 速度快，配置简单 | 免费额度有限 | 中小型项目 |
| Travis CI | SaaS | 配置简单，历史悠久 | 功能相对简单 | 开源项目 |
| Azure DevOps | SaaS | 微软生态集成 | 绑定 Azure | Azure 用户 |

### 详细对比

#### GitHub Actions

```yaml
# 优势
✅ 与 GitHub 无缝集成
✅ 免费额度：2000 分钟/月 (公开仓库无限)
✅ Marketplace 丰富模板
✅ 支持矩阵构建
✅ 社区活跃

# 劣势
❌ 仅限 GitHub 仓库
❌ 复杂流水线配置较繁琐
❌ 自托管 Runner 需要维护
```

#### GitLab CI

```yaml
# 优势
✅ 与 GitLab 深度集成
✅ 配置简洁 (.gitlab-ci.yml)
✅ 内置 Docker Registry
✅ 支持 Auto DevOps
✅ 可自托管

# 劣势
❌ 需要 GitLab
❌ 高级功能需要付费版
```

#### Jenkins

```yaml
# 优势
✅ 插件生态丰富 (1500+ 插件)
✅ 高度可定制
✅ 支持任何部署目标
✅ 完全免费开源

# 劣势
❌ 配置复杂 (Groovy 脚本)
❌ 维护成本高
❌ UI 较老旧
❌ 需要专门团队维护
```

---

## GitHub Actions 实战

### 基础配置

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

### 矩阵构建

```yaml
# .github/workflows/matrix-build.yml
name: Matrix Build

on: push

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [16, 18, 20]
        exclude:
          - os: windows-latest
            node-version: 16
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Test
        run: npm test
```

### Docker 构建与推送

```yaml
# .github/workflows/docker.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix=sha-
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 多环境部署

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Staging
        uses: azure/webapps-deploy@v2
        with:
          app-name: myapp-staging
          publish-profile: ${{ secrets.AZURE_STAGING_PROFILE }}
          package: .
      
      - name: Run smoke tests
        run: |
          curl -f https://myapp-staging.azurewebsites.net/health

  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    needs: deploy-staging
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Production
        uses: azure/webapps-deploy@v2
        with:
          app-name: myapp-production
          publish-profile: ${{ secrets.AZURE_PROD_PROFILE }}
          package: .
      
      - name: Run smoke tests
        run: |
          curl -f https://myapp.azurewebsites.net/health
      
      - name: Notify Slack
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ 生产环境部署成功: ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 定时任务

```yaml
# .github/workflows/scheduled.yml
name: Scheduled Tasks

on:
  schedule:
    # 每天 UTC 0 点执行
    - cron: '0 0 * * *'
  workflow_dispatch:  # 支持手动触发

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup old artifacts
        uses: actions/delete-package-versions@v4
        with:
          package-name: myapp
          package-type: container
          min-versions-to-keep: 10
          delete-only-untagged-versions: true

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

## GitLab CI 实战

### 基础配置

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"
  DOCKER_REGISTRY: registry.gitlab.com

lint:
  stage: lint
  image: node:${NODE_VERSION}-alpine
  script:
    - npm ci
    - npm run lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

test:
  stage: test
  image: node:${NODE_VERSION}-alpine
  script:
    - npm ci
    - npm test
  coverage: '/Lines\s*:\s*(\d+.\d+)\%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
  environment:
    name: production
    url: https://example.com
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### 模板复用

```yaml
# .gitlab/ci/templates/nodejs.yml
.nodejs_template: &nodejs_template
  image: node:18-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  before_script:
    - npm ci

# 使用模板
lint:
  <<: *nodejs_template
  script:
    - npm run lint

test:
  <<: *nodejs_template
  script:
    - npm test
```

### 并行任务

```yaml
# .gitlab-ci.yml
test:
  stage: test
  image: node:18-alpine
  parallel:
    matrix:
      - TEST_SUITE: [unit, integration, e2e]
  script:
    - npm ci
    - npm run test:${TEST_SUITE}
  artifacts:
    when: always
    reports:
      junit: reports/${TEST_SUITE}-junit.xml
```

---

## Jenkins 实战

### Jenkinsfile 基础

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
        }
    }
    
    environment {
        NODE_VERSION = '18'
        DOCKER_REGISTRY = 'registry.example.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Lint') {
            steps {
                sh 'npm ci'
                sh 'npm run lint'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'reports/*.xml'
                    publishCoverage adapters: [coberturaAdapter('coverage/cobertura-coverage.xml')]
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/myapp:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${DOCKER_REGISTRY}/myapp:${env.BUILD_ID}").push()
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp myapp=${DOCKER_REGISTRY}/myapp:${BUILD_ID}
                    kubectl rollout status deployment/myapp
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend channel: '#deployments', 
                     color: 'good', 
                     message: "✅ Build ${env.BUILD_ID} succeeded"
        }
        failure {
            slackSend channel: '#deployments', 
                     color: 'danger', 
                     message: "❌ Build ${env.BUILD_ID} failed"
        }
    }
}
```

### 多分支流水线

```groovy
// Jenkinsfile (Multibranch)
properties([
    pipelineTriggers([
        cron('H/30 * * * *')  // 每 30 分钟检查
    ])
])

pipeline {
    agent any
    
    stages {
        stage('Environment') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        env.ENVIRONMENT = 'production'
                    } else if (env.BRANCH_NAME == 'develop') {
                        env.ENVIRONMENT = 'staging'
                    } else {
                        env.ENVIRONMENT = 'dev'
                    }
                }
            }
        }
        
        stage('Build & Deploy') {
            steps {
                echo "Deploying to ${env.ENVIRONMENT}"
                // 部署逻辑
            }
        }
    }
}
```

### 共享库

```groovy
// vars/deployToK8s.groovy (共享库)
def call(String environment, String imageTag) {
    withKubeConfig([credentialsId: "k8s-${environment}-config"]) {
        sh """
            kubectl set image deployment/myapp myapp=${imageTag}
            kubectl rollout status deployment/myapp
        """
    }
}

// 使用共享库
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                deployToK8s('production', 'registry.example.com/myapp:1.0.0')
            }
        }
    }
}
```

---

## Docker + K8s 部署

### Dockerfile 最佳实践

```dockerfile
# 多阶段构建
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产镜像
FROM node:18-alpine

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules

USER nodejs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "dist/server.js"]
```

### Kubernetes 部署配置

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: registry.example.com/myapp:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
```

### Helm Chart 部署

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My Application Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"

# values.yaml
replicaCount: 3
image:
  repository: registry.example.com/myapp
  tag: latest
  pullPolicy: Always
service:
  type: LoadBalancer
  port: 80
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

# CI/CD 中使用 Helm
# .github/workflows/deploy-helm.yml
- name: Deploy with Helm
  run: |
    helm upgrade --install myapp ./helm/myapp \
      --namespace production \
      --set image.tag=${{ github.sha }} \
      --wait --timeout 5m
```

---

## 最佳实践

### 1. 分支策略

```
main (生产)
  ↑
  │ release/*
  │
develop (预发)
  ↑
  │ feature/*
  │ bugfix/*
  │
feature-branch (开发)
```

### 2. 版本管理

```bash
# 语义化版本
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ 向后兼容的 bug 修复
  │     └─────── 向后兼容的功能
  └───────────── 不兼容的 API 变更

# Git 标签
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

### 3. 密钥管理

```yaml
# ❌ 错误：硬编码密钥
env:
  DATABASE_PASSWORD: "supersecret123"

# ✅ 正确：使用密钥管理
# GitHub Actions
env:
  DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}

# GitLab CI
variables:
  DATABASE_PASSWORD: $DATABASE_PASSWORD_SECRET

# Jenkins
environment {
    DATABASE_PASSWORD = credentials('database-password')
}
```

### 4. 回滚策略

```yaml
# 自动回滚配置
deploy:
  steps:
    - name: Deploy
      run: kubectl apply -f deployment.yaml
    
    - name: Wait for rollout
      run: kubectl rollout status deployment/myapp --timeout=300s
    
    - name: Rollback on failure
      if: failure()
      run: |
        kubectl rollout undo deployment/myapp
        echo "已回滚到上一个稳定版本"
```

### 5. 监控告警

```yaml
# Prometheus 告警规则
groups:
- name: deployment
  rules:
  - alert: DeploymentFailed
    expr: kube_deployment_status_condition{condition="Available",status="false"} == 1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "部署失败"
      description: "Deployment {{ $labels.deployment }} 不可用"
  
  - alert: HighErrorRate
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "错误率过高"
      description: "错误率 {{ $value | humanizePercentage }}"
```

---

## 故障排查

### 常见问题与解决方案

#### 1. 构建失败

```bash
# 问题：npm install 失败
❌ npm ERR! code ERESOLVE

# 解决：
✅ 删除 package-lock.json 重新生成
✅ 使用 npm ci 代替 npm install
✅ 检查 Node.js 版本是否匹配

# 调试命令
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 2. 测试超时

```yaml
# 问题：测试在 CI 中超时
❌ Error: Process completed with exit code 124

# 解决：
✅ 增加超时时间
timeout-minutes: 30

✅ 优化测试
- 使用测试并行
- Mock 外部依赖
- 减少 E2E 测试数量
```

#### 3. 部署失败

```bash
# 问题：Kubernetes 部署卡住
❌ deployment "myapp" exceeded its progress deadline

# 排查步骤：
1. 查看 Pod 状态
kubectl get pods -l app=myapp

2. 查看 Pod 日志
kubectl logs deployment/myapp

3. 查看事件
kubectl describe deployment/myapp

4. 常见原因：
   - 镜像拉取失败 (ImagePullBackOff)
   - 健康检查失败 (CrashLoopBackOff)
   - 资源不足 (Pending)
   - 配置错误
```

#### 4. 环境变量问题

```bash
# 问题：环境变量未生效

# 排查：
1. 检查 Secret/ConfigMap 是否存在
kubectl get secret myapp-secrets
kubectl get configmap myapp-config

2. 检查 Deployment 引用
kubectl get deployment myapp -o yaml

3. 重启 Pod 使配置生效
kubectl rollout restart deployment/myapp
```

### 调试技巧

```yaml
# 启用调试模式
debug:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    # 启用 SSH 调试
    - name: Setup tmate session
      if: ${{ failure() }}
      uses: mxschmitt/action-tmate@v3
      timeout-minutes: 15
    
    # 打印详细日志
    - name: Debug info
      run: |
        echo "Runner: $RUNNER_OS"
        echo "Node: $(node --version)"
        echo "NPM: $(npm --version)"
        echo "Disk space: $(df -h)"
        echo "Memory: $(free -h)"
```

---

## 总结

### CI/CD 成熟度模型

```
Level 1: 手动部署
  └─ 脚本化部署流程

Level 2: 基础 CI
  └─ 自动构建 + 自动测试

Level 3: 持续交付
  └─ 自动部署到预发 + 手动批准生产

Level 4: 持续部署
  └─ 全自动部署到生产

Level 5: DevOps 文化
  └─ 监控 + 反馈 + 持续改进
```

### 关键指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| 部署频率 | 每天多次 | 部署次数/天 |
| 变更前置时间 | < 1 小时 | 提交到部署时间 |
| 变更失败率 | < 5% | 失败部署/总部署 |
| 恢复时间 | < 1 小时 | 故障到恢复时间 |

### 学习路径

```
Week 1-2: 基础概念
  - 理解 CI/CD 流程
  - 选择合适工具

Week 3-4: 实践入门
  - 配置第一个流水线
  - 实现自动测试

Month 2: 进阶实践
  - 多环境部署
  - Docker 容器化

Month 3: 生产就绪
  - 监控告警
  - 回滚机制
  - 安全扫描

Ongoing: 持续优化
  - 性能优化
  - 成本优化
  - 流程改进
```

---

## 参考资源

- 📚 书籍：《持续交付》
- 📚 书籍：《DevOps 实践指南》
- 🌐 GitHub Actions 文档：https://docs.github.com/actions
- 🌐 GitLab CI 文档：https://docs.gitlab.com/ee/ci/
- 🌐 Jenkins 文档：https://www.jenkins.io/doc/
- 🎥 视频：CI/CD 实战课程

---

*最后更新：2026-03-13*  
*作者：AI 技术团队*  
*标签：#CI/CD #DevOps #自动化部署 #GitHub Actions #Jenkins*
