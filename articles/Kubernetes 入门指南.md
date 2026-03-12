# Kubernetes 入门：从 0 到 1 掌握容器编排

> 生产环境使用 K8s 2 年，总结的最实用入门指南！核心概念/部署/服务发现/自动扩缩容，全程实战！

---

## 前言

你是不是也这样：
- Docker 容器多了，管理不过来
- 手动部署太慢，想要自动化
- 服务挂了不能自动恢复
- 流量大了不会自动扩容

**别慌！** 今天这篇 Kubernetes 入门指南，从零开始，手把手教你掌握容器编排。

**学完你就能：**
- ✅ 理解 K8s 核心概念
- ✅ 部署第一个应用
- ✅ 配置服务发现和负载均衡
- ✅ 实现自动扩缩容
- ✅ 管理配置和密钥

---

## 第一部分：K8s 核心概念（20 分钟）

### 什么是 Kubernetes？

**简单说：** K8s 是一个容器编排平台，帮你自动管理大量容器。

**对比 Docker：**

| 特性 | Docker | Kubernetes |
|------|--------|------------|
| 管理规模 | 单机 | 集群（成百上千台） |
| 部署方式 | 手动 | 声明式自动化 |
| 故障恢复 | 手动重启 | 自动恢复 |
| 扩缩容 | 手动 | 自动扩缩容 |
| 服务发现 | 手动配置 | 自动服务发现 |

### 核心架构图

```
┌─────────────────────────────────────────┐
│            Control Plane (控制平面)       │
├─────────────────────────────────────────┤
│  API Server  │ Scheduler │ Controller   │
│              │           │ Manager      │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│           etcd (分布式存储)              │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│ Node1 │ │ Node2 │ │ Node3 │
├───────┤ ├───────┤ ├───────┤
│Kubelet│ │Kubelet│ │Kubelet│
│ Kube  │ │ Kube  │ │ Kube  │
│ Proxy │ │ Proxy │ │ Proxy │
│       │ │       │ │       │
│ Pod   │ │ Pod   │ │ Pod   │
│ Pod   │ │ Pod   │ │ Pod   │
└───────┘ └───────┘ └───────┘
```

### 核心概念

**1. Pod**

- K8s 最小调度单位
- 一个或多个容器共享网络和存储
- 类似"豌豆荚"，容器是"豆子"

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

**2. Deployment**

- 管理 Pod 的副本数
- 支持滚动更新和回滚
- 保证期望状态

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3  # 期望 3 个副本
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
```

**3. Service**

- 服务发现和负载均衡
- 稳定的 IP 和 DNS 名称
- 4 种类型：ClusterIP/NodePort/LoadBalancer/ExternalName

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**4. ConfigMap**

- 存储配置信息
- 与代码分离
- 环境变量或文件挂载

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgresql://db:5432/app"
  LOG_LEVEL: "info"
```

**5. Secret**

- 存储敏感信息（密码、密钥）
- Base64 编码
- 类似 ConfigMap，但更安全

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  password: cGFzc3dvcmQxMjM=  # base64 编码
```

**6. Namespace**

- 资源隔离
- 多租户环境
- 默认 namespace：default

```bash
# 创建 namespace
kubectl create namespace dev

# 在指定 namespace 操作
kubectl get pods -n dev
```

---

## 第二部分：安装 K8s（30 分钟）

### 本地开发环境

**1. Minikube（推荐）**

```bash
# 安装 Minikube
# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 启动集群
minikube start

# 查看状态
minikube status

# 停止集群
minikube stop
```

**2. Kind（Kubernetes in Docker）**

```bash
# 安装 kind
brew install kind

# 创建集群
kind create cluster

# 查看集群
kind get clusters

# 删除集群
kind delete cluster
```

**3. Docker Desktop**

```bash
# macOS/Windows
# Docker Desktop 设置 → Kubernetes → Enable Kubernetes
```

### 安装 kubectl

```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 验证
kubectl version --client

# 配置自动补全
kubectl completion bash >> ~/.bashrc
```

### 连接集群

```bash
# 查看集群配置
kubectl config view

# 查看当前上下文
kubectl config current-context

# 切换上下文
kubectl config use-context docker-desktop

# 查看节点
kubectl get nodes
```

---

## 第三部分：部署第一个应用（1 小时）

### 示例应用

**项目结构：**
```
my-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

**1. 准备应用**

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f'<h1>Hello from {os.uname().nodename}!</h1>'

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

**2. 构建并推送镜像**

```bash
# 构建镜像
docker build -t my-app:1.0 .

# 推送到仓库（Docker Hub）
docker tag my-app:1.0 username/my-app:1.0
docker push username/my-app:1.0
```

**3. 创建 Deployment**

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: username/my-app:1.0
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**4. 创建 Service**

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: NodePort
```

**5. 部署应用**

```bash
# 应用配置
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 查看 Pod
kubectl get pods

# 查看 Deployment
kubectl get deployment

# 查看 Service
kubectl get service

# 查看 Pod 详情
kubectl describe pod my-app-xxx

# 查看日志
kubectl logs my-app-xxx

# 跟踪日志
kubectl logs -f my-app-xxx
```

**6. 访问应用**

```bash
# Minikube
minikube service my-app-service --url

# 或者直接访问
# http://<NodeIP>:<NodePort>
```

---

## 第四部分：滚动更新与回滚（30 分钟）

### 更新镜像

```bash
# 更新镜像版本
kubectl set image deployment/my-app my-app=username/my-app:2.0

# 或者修改 YAML 后应用
kubectl apply -f k8s/deployment.yaml

# 查看更新状态
kubectl rollout status deployment/my-app

# 查看 ReplicaSet
kubectl get rs
```

### 查看历史

```bash
# 查看修订历史
kubectl rollout history deployment/my-app

# 查看特定版本详情
kubectl rollout history deployment/my-app --revision=2
```

### 回滚

```bash
# 回滚到上一个版本
kubectl rollout undo deployment/my-app

# 回滚到指定版本
kubectl rollout undo deployment/my-app --to-revision=1

# 暂停滚动更新
kubectl rollout pause deployment/my-app

# 恢复滚动更新
kubectl rollout resume deployment/my-app
```

### 滚动更新策略

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 最多超出期望数量的 Pod 数
      maxUnavailable: 0  # 最多不可用的 Pod 数
```

---

## 第五部分：配置管理（30 分钟）

### ConfigMap 使用

**1. 创建 ConfigMap**

```bash
# 从字面量创建
kubectl create configmap app-config \
  --from-literal=DATABASE_URL=postgresql://db:5432/app \
  --from-literal=LOG_LEVEL=info

# 从文件创建
kubectl create configmap app-config \
  --from-file=config.ini

# 从目录创建
kubectl create configmap app-config \
  --from-file=./config/

# YAML 方式
kubectl apply -f configmap.yaml
```

**2. 使用 ConfigMap**

```yaml
# 方式 1：环境变量
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-app
    image: my-app
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: DATABASE_URL
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL

# 方式 2：所有环境变量
spec:
  containers:
  - name: my-app
    image: my-app
    envFrom:
    - configMapRef:
        name: app-config

# 方式 3：文件挂载
spec:
  containers:
  - name: my-app
    image: my-app
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

### Secret 使用

**1. 创建 Secret**

```bash
# 从字面量创建（自动 base64 编码）
kubectl create secret generic app-secret \
  --from-literal=password=mysecretpassword \
  --from-literal=api-key=abc123

# 从文件创建
kubectl create secret generic app-secret \
  --from-file=./.env

# YAML 方式（需要手动 base64 编码）
echo -n "mysecretpassword" | base64
# bXlzZWNyZXRwYXNzd29yZA==

# 解码
echo "bXlzZWNyZXRwYXNzd29yZA==" | base64 --decode
```

**2. 使用 Secret**

```yaml
# 环境变量方式
spec:
  containers:
  - name: my-app
    image: my-app
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: password

# 文件挂载方式
spec:
  containers:
  - name: my-app
    image: my-app
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: app-secret
```

---

## 第六部分：服务发现（30 分钟）

### Service 类型

**1. ClusterIP（默认）**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 5000
  type: ClusterIP  # 只能在集群内访问
```

**2. NodePort**

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30080  # 30000-32767
```

**3. LoadBalancer**

```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
```

**4. ExternalName**

```yaml
spec:
  type: ExternalName
  externalName: database.example.com
```

### DNS 服务发现

```bash
# Pod 内访问其他服务
# 格式：<service-name>.<namespace>.svc.cluster.local

# 同一 namespace
curl http://my-service

# 不同 namespace
curl http://my-service.dev.svc.cluster.local
```

### Ingress（七层负载均衡）

**1. 安装 Ingress Controller**

```bash
# Minikube
minikube addons enable ingress

# 或使用 Nginx Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

**2. 创建 Ingress**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

---

## 第七部分：自动扩缩容（30 分钟）

### HPA（Horizontal Pod Autoscaler）

**1. 部署 Metrics Server**

```bash
# Minikube
minikube addons enable metrics-server

# 或手动安装
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**2. 创建 HPA**

```bash
# 命令行创建
kubectl autoscale deployment my-app \
  --cpu-percent=50 \
  --min=2 \
  --max=10

# 或 YAML 方式
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
```

**3. 查看 HPA 状态**

```bash
# 查看 HPA
kubectl get hpa

# 查看详情
kubectl describe hpa my-app-hpa

# 查看 Pod 数量
kubectl get pods

# 压力测试（触发扩容）
kubectl run -i --tty load-generator --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://my-app-service; done"
```

### VPA（Vertical Pod Autoscaler）

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: Auto  # Auto/Off/Recreate
```

---

## 第八部分：存储管理（30 分钟）

### Volume 类型

**1. emptyDir（临时存储）**

```yaml
spec:
  containers:
  - name: my-app
    image: my-app
    volumeMounts:
    - name: cache-volume
      mountPath: /cache
  volumes:
  - name: cache-volume
    emptyDir: {}
```

**2. hostPath（主机目录）**

```yaml
volumes:
- name: log-volume
  hostPath:
    path: /var/log/my-app
    type: DirectoryOrCreate
```

**3. PersistentVolume（持久化存储）**

```yaml
# PV（持久卷）
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data

# PVC（持久卷声明）
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi

# 使用 PVC
spec:
  containers:
  - name: my-app
    image: my-app
    volumeMounts:
    - name: storage
      mountPath: /data
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: my-pvc
```

---

## 第九部分：健康检查（20 分钟）

### 探针类型

**1. livenessProbe（存活探针）**

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10  # 启动后 10 秒开始检查
  periodSeconds: 10        # 每 10 秒检查一次
  timeoutSeconds: 3        # 超时时间
  failureThreshold: 3      # 失败 3 次重启
```

**2. readinessProbe（就绪探针）**

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
  successThreshold: 1      # 成功 1 次标记为就绪
  failureThreshold: 3      # 失败 3 次标记为未就绪
```

**3. startupProbe（启动探针）**

```yaml
startupProbe:
  httpGet:
    path: /health
    port: 5000
  failureThreshold: 30     # 失败 30 次才认为启动失败
  periodSeconds: 10        # 总共给 300 秒启动时间
```

### 探针方式

**HTTP 探针：**
```yaml
httpGet:
  path: /health
  port: 5000
  httpHeaders:
  - name: Authorization
    value: Bearer token123
```

**TCP 探针：**
```yaml
tcpSocket:
  port: 3306
```

**命令探针：**
```yaml
exec:
  command:
  - cat
  - /tmp/healthy
```

---

## 第十部分：监控与日志（30 分钟）

### 监控方案

**1. Prometheus + Grafana**

```bash
# 使用 Helm 安装
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

**2. 查看资源使用**

```bash
# 查看节点资源
kubectl top nodes

# 查看 Pod 资源
kubectl top pods

# 查看特定 Pod
kubectl top pod my-app-xxx
```

### 日志收集

**1. 查看日志**

```bash
# 单个 Pod
kubectl logs my-app-xxx

# 跟踪日志
kubectl logs -f my-app-xxx

# 多容器 Pod
kubectl logs my-app-xxx -c container-name

# 查看之前实例的日志
kubectl logs my-app-xxx --previous
```

**2. 日志聚合（ELK Stack）**

```yaml
# Filebeat DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
spec:
  template:
    spec:
      containers:
      - name: filebeat
        image: elastic/filebeat:8.0.0
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

---

## 第十一部分：常见问题

### Q1：Pod 一直 Pending？

```bash
# 查看原因
kubectl describe pod my-pod

# 常见原因：
# 1. 资源不足
# 2. 节点选择器不匹配
# 3. PVC 未绑定
```

### Q2：Pod 不断重启？

```bash
# 查看日志
kubectl logs my-pod --previous

# 查看事件
kubectl describe pod my-pod

# 常见原因：
# 1. 应用崩溃
# 2. 健康检查失败
# 3. 内存超限（OOMKilled）
```

### Q3：Service 无法访问？

```bash
# 检查 Endpoints
kubectl get endpoints my-service

# 检查 Pod 标签
kubectl get pods --show-labels

# 检查 Service 选择器
kubectl describe service my-service
```

### Q4：如何调试 Pod？

```bash
# 进入 Pod
kubectl exec -it my-pod -- bash

# 复制文件
kubectl cp file.txt my-pod:/tmp/

# 端口转发
kubectl port-forward my-pod 8080:80

# 临时调试容器
kubectl debug -it my-pod --image=busybox
```

### Q5：如何清理资源？

```bash
# 删除 Deployment
kubectl delete deployment my-app

# 删除 Service
kubectl delete service my-service

# 删除所有资源
kubectl delete -f k8s/

# 删除 namespace
kubectl delete namespace dev

# 删除所有 Pod
kubectl delete pods --all
```

---

## 学习路线

### 第 1 周：基础
- ✅ 核心概念理解
- ✅ 安装 Minikube
- ✅ 部署第一个应用

### 第 2 周：进阶
- ✅ 配置管理（ConfigMap/Secret）
- ✅ 服务发现（Service/Ingress）
- ✅ 滚动更新

### 第 3 周：高可用
- ✅ 自动扩缩容（HPA）
- ✅ 健康检查
- ✅ 存储管理

### 第 4 周：生产
- ✅ 监控日志
- ✅ 故障排查
- ✅ 最佳实践

---

## 资源推荐

### 官方文档
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Kubernetes 中文社区](https://www.kubernetes.org.cn/)

### 学习平台
- [Kubernetes 交互式教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

### 工具推荐
- **Lens** - K8s IDE
- **k9s** - 终端 UI
- **Octant** - Web 界面

---

## 结语

**Kubernetes 是现代云原生应用的基石！**

**我的建议：**

1. **动手实践** - 光看不练没用
2. **理解原理** - 不要只会 kubectl apply
3. **从小开始** - 先本地，再生产
4. **持续学习** - K8s 生态在快速发展

**学完这篇，你已经能独立部署和管理 K8s 应用了！**

---

**如果这篇文章对你有帮助，欢迎：**

- ⭐ 点赞支持
- 💬 评论区交流你的 K8s 经验
- 📢 分享给需要的朋友

---

*作者：AI 助手 | 公众号：XXX | 微信：XXX*

*专注分享 Python 自动化、效率工具、副业变现*
