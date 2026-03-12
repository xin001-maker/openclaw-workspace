# Redis 实战：从入门到高可用架构

> 生产环境使用 Redis 3 年，总结的最实用指南！缓存设计/持久化/集群/故障排查，全程实战！

---

## 前言

你是不是也这样：
- 数据库压力大，想加缓存但不知道怎么设计
- 缓存穿透/击穿/雪崩，遇到问题不知道咋解决
- Redis 持久化配置不懂，怕数据丢失
- 想搭建集群，但不知道从哪开始

**别慌！** 今天这篇 Redis 实战指南，从基础到高可用架构，都是我生产环境的血泪经验。

**学完你就能：**
- ✅ 掌握 5 种数据类型和应用场景
- ✅ 设计合理的缓存架构
- ✅ 解决缓存穿透/击穿/雪崩
- ✅ 配置持久化和主从复制
- ✅ 搭建 Redis Cluster 集群

---

## 第一部分：Redis 核心概念（15 分钟）

### 什么是 Redis？

**简单说：** Redis 是一个内存数据库，速度超快！

**对比 MySQL：**

| 特性 | Redis | MySQL |
|------|-------|-------|
| 存储介质 | 内存 | 磁盘 |
| 读取速度 | 10 万 QPS | 1 万 QPS |
| 数据结构 | 丰富（5 种） | 单一（表） |
| 持久化 | 可选 | 必须 |
| 适用场景 | 缓存/队列/计数 | 主存储 |

### 5 种核心数据类型

**1. String（字符串）**

```bash
# 基本操作
SET user:1001 '{"name": "张三", "age": 25}'
GET user:1001

# 计数器（原子操作）
INCR article:123:views  # 文章阅读量 +1
INCRBY user:1001:score 10  # 分数 +10

# 设置过期时间
SET session:abc123 '{"user_id": 1001}' EX 3600  # 1 小时后过期

# 应用场景：
# - 缓存用户信息
# - 计数器（阅读/点赞/评论）
# - 分布式锁
# - Session 存储
```

**2. Hash（哈希）**

```bash
# 存储对象
HSET user:1001 name "张三"
HSET user:1001 age 25
HSET user:1001 email "zhangsan@example.com"

# 获取字段
HGET user:1001 name
HGETALL user:1001

# 批量操作
HMSET user:1002 name "李四" age 30 email "lisi@example.com"
HMGET user:1002 name age

# 应用场景：
# - 存储对象（比 String 更省内存）
# - 购物车
# - 用户配置
```

**3. List（列表）**

```bash
# 压入元素
LPUSH queue:tasks "task1" "task2" "task3"

# 弹出元素
RPOP queue:tasks  # 从右边弹出（FIFO 队列）

# 范围查询
LRANGE queue:tasks 0 -1  # 查看所有元素

# 阻塞弹出（消息队列）
BRPOP queue:tasks 0  # 阻塞直到有元素

# 应用场景：
# - 消息队列
# - 最新列表（最新文章/评论）
# - 时间线（朋友圈/微博）
```

**4. Set（集合）**

```bash
# 添加元素（自动去重）
SADD article:123:likes user1001
SADD article:123:likes user1002
SADD article:123:likes user1001  # 重复，不会添加

# 获取元素
SMEMBERS article:123:likes

# 集合运算
SINTER set1 set2  # 交集（共同好友）
SUNION set1 set2  # 并集
SDIFF set1 set2   # 差集

# 应用场景：
# - 点赞/收藏（去重）
# - 好友关系
# - 标签系统
```

**5. ZSet（有序集合）**

```bash
# 添加元素（带分数）
ZADD leaderboard:game1 1000 "player1"
ZADD leaderboard:game1 2000 "player2"
ZADD leaderboard:game1 1500 "player3"

# 获取排名
ZREVRANK leaderboard:game1 "player1"  # 排名（从高到低）
ZREVRANGE leaderboard:game1 0 9 WITHSCORES  # 前 10 名

# 分数范围
ZRANGEBYSCORE leaderboard:game1 1000 2000

# 应用场景：
# - 排行榜（游戏/销售）
# - 优先级队列
# - 延时任务
```

---

## 第二部分：缓存设计实战（1 小时）

### 缓存模式

**1. Cache Aside（最常用）**

```python
def get_user(user_id):
    # 1. 先读缓存
    key = f'user:{user_id}'
    user = redis.get(key)
    if user:
        return json.loads(user)
    
    # 2. 缓存未命中，读数据库
    user = db.query('SELECT * FROM users WHERE id = %s', user_id)
    
    # 3. 写入缓存
    if user:
        redis.setex(key, 3600, json.dumps(user))
    
    return user

def update_user(user_id, data):
    # 1. 更新数据库
    db.update('UPDATE users SET ... WHERE id = %s', user_id)
    
    # 2. 删除缓存（下次读取时重建）
    redis.delete(f'user:{user_id}')
```

**优点：** 简单，一致性好  
**缺点：** 第一次读取慢

**2. Read Through**

```python
# Redis 自动处理缓存未命中
# 需要配置 Redis 模块或使用代理

def get_user(user_id):
    # Redis 自动：
    # 1. 检查缓存
    # 2. 未命中时自动查询数据库
    # 3. 写入缓存并返回
    return redis.get(f'user:{user_id}')
```

**优点：** 应用层简单  
**缺点：** 需要额外组件

**3. Write Through**

```python
def update_user(user_id, data):
    # 同时更新缓存和数据库
    db.update('UPDATE users SET ... WHERE id = %s', user_id)
    redis.set(f'user:{user_id}', json.dumps(data))
```

**优点：** 数据一致性好  
**缺点：** 写入慢

**4. Write Behind**

```python
def update_user(user_id, data):
    # 先更新缓存
    redis.set(f'user:{user_id}', json.dumps(data))
    
    # 异步写入数据库（批量）
    # Redis 定期将数据刷到数据库
```

**优点：** 写入快  
**缺点：** 可能丢失数据

### 缓存粒度选择

**1. 整表缓存**

```python
# 适合：小表，不常变化
def get_all_products():
    products = redis.get('products:all')
    if products:
        return json.loads(products)
    
    products = db.query('SELECT * FROM products')
    redis.setex('products:all', 3600, json.dumps(products))
    return products
```

**2. 单行缓存**

```python
# 适合：大表，随机访问
def get_product(product_id):
    product = redis.get(f'product:{product_id}')
    if product:
        return json.loads(product)
    
    product = db.query('SELECT * FROM products WHERE id = %s', product_id)
    redis.setex(f'product:{product_id}', 3600, json.dumps(product))
    return product
```

**3. 字段级缓存**

```python
# 适合：热点字段
def get_product_info(product_id):
    # 只缓存热点字段
    data = redis.hgetall(f'product:{product_id}:info')
    if data:
        return {
            'name': data['name'],
            'price': data['price'],
            'stock': data['stock']
        }
    
    product = db.query('SELECT name, price, stock FROM products WHERE id = %s', product_id)
    redis.hmset(f'product:{product_id}:info', product)
    redis.expire(f'product:{product_id}:info', 3600)
    return product
```

### 缓存过期策略

**1. 固定过期时间**

```python
# 简单，但可能导致同时失效
redis.setex('key', 3600, value)  # 1 小时后过期
```

**2. 随机过期时间**

```python
# 避免同时失效
import random
expire_time = 3600 + random.randint(0, 600)  # 1-1.1 小时
redis.setex('key', expire_time, value)
```

**3. 永不过期 + 异步更新**

```python
# 缓存永不过期，后台异步更新
redis.set('key', value)  # 不过期

# 后台任务定期更新
def refresh_cache():
    while True:
        data = db.query('SELECT * FROM hot_data')
        redis.set('hot_data', json.dumps(data))
        time.sleep(300)  # 每 5 分钟更新
```

---

## 第三部分：缓存问题解决方案（1 小时）

### 问题 1：缓存穿透

**现象：** 查询不存在的数据，缓存不命中，请求直达数据库

**原因：**
- 恶意攻击（故意查询不存在的 ID）
- 业务逻辑问题（查询已删除的数据）

**解决方案：**

**1. 缓存空值**

```python
def get_user(user_id):
    key = f'user:{user_id}'
    
    # 检查缓存
    user = redis.get(key)
    if user == 'NULL':  # 缓存了空值
        return None
    if user:
        return json.loads(user)
    
    # 查询数据库
    user = db.query('SELECT * FROM users WHERE id = %s', user_id)
    
    if not user:
        # 缓存空值，防止再次查询
        redis.setex(key, 300, 'NULL')  # 5 分钟
        return None
    
    redis.setex(key, 3600, json.dumps(user))
    return user
```

**2. 布隆过滤器**

```python
from pybloom_live import BloomFilter

# 初始化布隆过滤器
bloom = BloomFilter(capacity=1000000, error_rate=0.001)

# 添加存在的 ID
for user_id in db.query('SELECT id FROM users'):
    bloom.add(user_id)

def get_user(user_id):
    # 先通过布隆过滤器检查
    if user_id not in bloom:
        return None  # 肯定不存在
    
    # 继续正常流程
    ...
```

**3. 接口层校验**

```python
def get_user(user_id):
    # 参数校验
    if not user_id or user_id <= 0:
        raise ValueError('Invalid user_id')
    
    # 继续正常流程
    ...
```

### 问题 2：缓存击穿

**现象：** 热点 key 过期瞬间，大量请求直达数据库

**原因：**
- 热点数据过期
- 高并发访问

**解决方案：**

**1. 互斥锁**

```python
import redis
import time

def get_user(user_id):
    key = f'user:{user_id}'
    lock_key = f'lock:user:{user_id}'
    
    # 检查缓存
    user = redis.get(key)
    if user:
        return json.loads(user)
    
    # 获取互斥锁
    lock = redis.lock(lock_key, timeout=10)
    if lock.acquire(blocking=False):
        try:
            # 双重检查
            user = redis.get(key)
            if user:
                return json.loads(user)
            
            # 查询数据库
            user = db.query('SELECT * FROM users WHERE id = %s', user_id)
            redis.setex(key, 3600, json.dumps(user))
            return user
        finally:
            lock.release()
    else:
        # 没抢到锁，等待重试
        time.sleep(0.1)
        return get_user(user_id)
```

**2. 逻辑过期**

```python
def get_user(user_id):
    key = f'user:{user_id}'
    
    # 获取缓存数据（包含过期时间）
    data = redis.get(key)
    if data:
        data = json.loads(data)
        expire_at = data.get('expire_at', 0)
        
        # 检查是否逻辑过期
        if time.time() < expire_at:
            return data['user']
        
        # 异步更新（不阻塞）
        if redis.lock(f'lock:{key}', timeout=10).acquire(blocking=False):
            threading.Thread(target=refresh_user, args=(user_id,)).start()
        
        return data['user']
    
    # 缓存未命中
    return refresh_user(user_id)

def refresh_user(user_id):
    user = db.query('SELECT * FROM users WHERE id = %s', user_id)
    data = {
        'user': user,
        'expire_at': time.time() + 3600
    }
    redis.setex(f'user:{user_id}', 7200, json.dumps(data))
```

### 问题 3：缓存雪崩

**现象：** 大量 key 同时过期，数据库压力激增

**原因：**
- 大量 key 设置相同过期时间
- Redis 宕机

**解决方案：**

**1. 随机过期时间**

```python
def cache_data(key, data, base_expire=3600):
    # 添加随机时间（±10%）
    expire = base_expire + random.randint(-360, 360)
    redis.setex(key, expire, json.dumps(data))
```

**2. 多级缓存**

```python
# 本地缓存 + Redis
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_local(user_id):
    return get_user_redis(user_id)

def get_user_redis(user_id):
    user = redis.get(f'user:{user_id}')
    if user:
        return json.loads(user)
    
    user = db.query('SELECT * FROM users WHERE id = %s', user_id)
    redis.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user
```

**3. 高可用架构**

```
应用 → Redis 主从 + 哨兵 → 数据库
       ↓
     自动故障转移
```

---

## 第四部分：持久化配置（30 分钟）

### RDB（快照）

**原理：** 定期生成数据快照

**配置：**

```conf
# redis.conf

# 保存条件（满足任一即触发）
save 900 1      # 900 秒内至少 1 个 key 变化
save 300 10     # 300 秒内至少 10 个 key 变化
save 60 10000   # 60 秒内至少 10000 个 key 变化

# RDB 文件名
dbfilename dump.rdb

# 工作目录
dir /var/lib/redis

# 压缩
rdbcompression yes

# 校验和
rdbchecksum yes
```

**优点：**
- ✅ 文件紧凑，适合备份
- ✅ 恢复速度快
- ✅ 对性能影响小

**缺点：**
- ❌ 可能丢失最后一次快照后的数据
- ❌ 大数据量时 fork 耗时

### AOF（追加日志）

**原理：** 记录每个写操作

**配置：**

```conf
# redis.conf

# 开启 AOF
appendonly yes

# 文件名
appendfilename "appendonly.aof"

# 同步策略
# always: 每次写入都同步（最安全，最慢）
# everysec: 每秒同步（推荐）
# no: 由操作系统决定（最快，可能丢数据）
appendfsync everysec

# AOF 重写
auto-aof-rewrite-percentage 100  # 增长 100% 时重写
auto-aof-rewrite-min-size 64mb   # 最小 64MB 才重写
```

**优点：**
- ✅ 数据更安全（最多丢 1 秒）
- ✅ 日志可读

**缺点：**
- ❌ 文件较大
- ❌ 恢复速度慢

### 混合持久化（Redis 4.0+）

```conf
# 结合 RDB 和 AOF 的优点
aof-use-rdb-preamble yes
```

**格式：**
```
AOF 文件 = RDB 快照 + 增量 AOF 日志
```

**优点：**
- ✅ 恢复快（RDB 部分）
- ✅ 数据全（AOF 部分）

### 持久化选择建议

| 场景 | 推荐方案 |
|------|----------|
| 纯缓存 | 关闭持久化 |
| 一般业务 | RDB + AOF（everysec） |
| 金融级 | AOF（always） |
| 大数据量 | RDB 为主，AOF 为辅 |

---

## 第五部分：主从复制（30 分钟）

### 架构

```
Master（写） → Slave1（读）
            → Slave2（读）
            → Slave3（读）
```

### 配置步骤

**1. Master 配置**

```conf
# redis-master.conf
bind 0.0.0.0
port 6379
requirepass master_password
```

**2. Slave 配置**

```conf
# redis-slave.conf
bind 0.0.0.0
port 6379
replicaof master_ip 6379
masterauth master_password
replica-read-only yes
```

**3. 启动**

```bash
# 启动 Master
redis-server redis-master.conf

# 启动 Slave
redis-server redis-slave.conf
```

**4. 验证**

```bash
# 在 Master 上
redis-cli -a master_password
> INFO replication
# Replication
# role:master
# connected_slaves:2

# 在 Slave 上
redis-cli
> INFO replication
# Replication
# role:slave
# master_host:master_ip
# master_port:6379
# master_link_status:up
```

### 读写分离

**应用层实现：**

```python
class RedisClient:
    def __init__(self):
        self.master = redis.Redis(host='master', password='master_password')
        self.slaves = [
            redis.Redis(host='slave1'),
            redis.Redis(host='slave2')
        ]
        self.slave_index = 0
    
    def write(self, key, value):
        # 写操作走 Master
        return self.master.set(key, value)
    
    def read(self, key):
        # 读操作轮询 Slave
        slave = self.slaves[self.slave_index]
        self.slave_index = (self.slave_index + 1) % len(self.slaves)
        return slave.get(key)
```

### 主从延迟问题

**原因：**
- 网络延迟
- Master 写入量大
- Slave 负载高

**解决：**
1. 优化网络（同机房部署）
2. 限制 Master 写入速度
3. Slave 不处理重任务
4. 监控延迟（`INFO replication`）

---

## 第六部分：哨兵模式（30 分钟）

### 架构

```
Sentinel1 ─┬─ 监控 ─ Master
Sentinel2 ─┤         │
Sentinel3 ─┴─         ├─ Slave1
                      └─ Slave2
```

### 配置步骤

**1. Sentinel 配置**

```conf
# sentinel.conf
port 26379
sentinel monitor mymaster master_ip 6379 2
sentinel auth-pass mymaster master_password
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000
```

**参数说明：**
- `sentinel monitor mymaster master_ip 6379 2`
  - 监控名称：mymaster
  - Master 地址：master_ip:6379
  - 法定人数：2（至少 2 个 Sentinel 同意才故障转移）

- `down-after-milliseconds`：5 秒无响应认为宕机
- `parallel-syncs`：故障转移时同时同步的 Slave 数
- `failover-timeout`：故障转移超时时间

**2. 启动 Sentinel**

```bash
redis-sentinel sentinel.conf
```

**3. 验证**

```bash
# 查看 Master 信息
redis-cli -p 26379
> SENTINEL master mymaster
# name=mymaster
# ip=master_ip
# port=6379
# flags=master
# num-slaves=2

# 查看 Slave 列表
> SENTINEL slaves mymaster

# 手动故障转移
> SENTINEL failover mymaster
```

### 应用连接

```python
import redis
from redis.sentinel import Sentinel

# 连接 Sentinel
sentinel = Sentinel([('sentinel1', 26379),
                     ('sentinel2', 26379),
                     ('sentinel3', 26379)],
                    socket_timeout=0.1)

# 获取 Master（写）
master = sentinel.master_for('mymaster', password='master_password')

# 获取 Slave（读）
slave = sentinel.slave_for('mymaster')

# 使用
master.set('key', 'value')
value = slave.get('key')
```

---

## 第七部分：Redis Cluster（1 小时）

### 架构

```
Client
  │
  ├─ Node1 (0-5460) ─ Master1 + Slave1
  ├─ Node2 (5461-10922) ─ Master2 + Slave2
  └─ Node3 (10923-16383) ─ Master3 + Slave3
```

### 创建集群

**1. 准备节点**

```conf
# redis-node1.conf
port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

**2. 启动节点**

```bash
redis-server redis-node1.conf
redis-server redis-node2.conf
redis-server redis-node3.conf
redis-server redis-node4.conf  # Slave
redis-server redis-node5.conf  # Slave
redis-server redis-node6.conf  # Slave
```

**3. 创建集群**

```bash
# Redis 5.0+
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

**4. 连接集群**

```bash
redis-cli -c -p 7000
> CLUSTER info
> CLUSTER nodes
```

### 应用连接

```python
from redis.cluster import RedisCluster

# 连接集群
rc = RedisCluster(startup_nodes=[
    {'host': '127.0.0.1', 'port': 7000},
    {'host': '127.0.0.1', 'port': 7001},
    {'host': '127.0.0.1', 'port': 7002}
])

# 使用（自动路由到正确节点）
rc.set('key1', 'value1')
rc.get('key1')
```

### 扩容

**1. 添加 Master 节点**

```bash
# 启动新节点
redis-server redis-node7.conf

# 添加到集群
redis-cli --cluster add-node 127.0.0.1:7006 127.0.0.1:7000

# 重新分片
redis-cli --cluster reshard 127.0.0.1:7000
```

**2. 添加 Slave 节点**

```bash
redis-cli --cluster add-node 127.0.0.1:7007 127.0.0.1:7000 \
  --cluster-slave --cluster-master-id <master_node_id>
```

### 故障转移

```bash
# 手动故障转移
redis-cli --cluster failover 127.0.0.1:7001

# 检查集群状态
redis-cli --cluster check 127.0.0.1:7000
```

---

## 第八部分：性能优化（30 分钟）

### 内存优化

**1. 使用合适的数据结构**

```python
# ❌ 差：String 存储对象
redis.set('user:1', '{"name": "张三", "age": 25}')

# ✅ 好：Hash 更省内存
redis.hset('user:1', 'name', '张三')
redis.hset('user:1', 'age', 25)
```

**2. 开启内存淘汰**

```conf
# redis.conf

# 最大内存
maxmemory 2gb

# 淘汰策略
# volatile-lru: 淘汰有过期时间的 key（LRU）
# allkeys-lru: 淘汰所有 key（推荐用于缓存）
# volatile-ttl: 淘汰即将过期的 key
# volatile-random: 随机淘汰有过期时间的 key
# allkeys-random: 随机淘汰
# noeviction: 不淘汰（默认）
maxmemory-policy allkeys-lru
```

**3. 内存分析**

```bash
# 查看内存使用
redis-cli INFO memory

# 查看大 key
redis-cli --bigkeys

# 使用 memory 命令
redis-cli MEMORY USAGE user:1001
redis-cli MEMORY DOCTOR
```

### 性能优化

**1. 批量操作**

```python
# ❌ 差：单次操作
for i in range(1000):
    redis.set(f'key:{i}', i)

# ✅ 好：管道批量
pipe = redis.pipeline()
for i in range(1000):
    pipe.set(f'key:{i}', i)
pipe.execute()
# 快 10 倍！
```

**2. 避免慢命令**

```bash
# ❌ 慢命令（O(N)）
KEYS *              # 扫描所有 key
HGETALL large_hash  # 获取大 hash 所有字段
SMEMBERS large_set  # 获取大 set 所有成员

# ✅ 替代方案
SCAN 0 MATCH * COUNT 100  # 迭代扫描
HSCAN key 0 COUNT 100     # 迭代 hash
SSCAN key 0 COUNT 100     # 迭代 set
```

**3. 禁用危险命令**

```conf
# redis.conf
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command CONFIG ""
rename-command KEYS ""
```

### 网络优化

**1. 调整 TCP 参数**

```conf
# redis.conf
tcp-backlog 511
tcp-keepalive 300
```

**2. 绑定 CPU**

```bash
# 绑定到特定 CPU 核心
taskset -c 0-3 redis-server redis.conf
```

---

## 第九部分：监控与告警（30 分钟）

### 监控指标

**1. 基础指标**
- 内存使用率
- CPU 使用率
- 连接数
- 网络流量

**2. Redis 指标**
- QPS
- 命中率
- 淘汰 key 数量
- 持久化状态
- 主从延迟

**3. 业务指标**
- 缓存命中率
- 平均响应时间
- 错误率

### 监控工具

**1. Redis 自带命令**

```bash
# 实时信息
redis-cli INFO

# 实时监控
redis-cli --stat

# 慢查询日志
redis-cli CONFIG GET slowlog-log-slower-than
redis-cli SLOWLOG GET 10

# 实时命令监控
redis-cli MONITOR  # 生产环境慎用
```

**2. Redis Sentinel**

```bash
# 查看 Master 信息
redis-cli -p 26379 SENTINEL master mymaster

# 查看 Slave 列表
redis-cli -p 26379 SENTINEL slaves mymaster
```

**3. 第三方工具**

- **RedisInsight** - 官方 GUI 工具
- **Redis Desktop Manager** - 图形化管理
- **Prometheus + Grafana** - 监控告警

### Prometheus 配置

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### 告警规则

```yaml
# alerting_rules.yml
groups:
- name: redis
  rules:
  - alert: RedisDown
    expr: redis_up == 0
    for: 1m
    annotations:
      summary: "Redis 实例 {{ $labels.instance }} 宕机"
  
  - alert: RedisHighMemory
    expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
    for: 5m
    annotations:
      summary: "Redis 内存使用率超过 90%"
  
  - alert: RedisLowHitRate
    expr: redis_keyspace_hits / (redis_keyspace_hits + redis_keyspace_misses) < 0.8
    for: 10m
    annotations:
      summary: "Redis 缓存命中率低于 80%"
```

---

## 第十部分：常见问题

### Q1：Redis 为什么快？

```
1. 纯内存操作
2. 单线程（无锁竞争）
3. IO 多路复用
4. 高效数据结构
```

### Q2：Redis 是单线程还是多线程？

```
- 网络 IO 和命令执行：单线程
- 持久化（RDB/AOF）：多线程（Redis 4.0+）
- 删除操作：异步后台线程（Redis 4.0+）
```

### Q3：如何保证缓存与数据库一致性？

```
1. Cache Aside + 延时双删
2. 监听 binlog 异步更新缓存（Canal）
3. 强一致性场景：直接读数据库
```

### Q4：Redis 宕机怎么处理？

```
1. 哨兵自动故障转移
2. 持久化恢复数据
3. 降级：直接查数据库
4. 限流：保护数据库
```

### Q5：如何发现大 key？

```bash
# 方法 1：redis-cli
redis-cli --bigkeys

# 方法 2：memory 命令
redis-cli MEMORY USAGE key_name

# 方法 3：监控分析
# 使用 RedisInsight 等工具
```

---

## 学习路线

### 第 1 周：基础
- ✅ 5 种数据类型
- ✅ 基本命令
- ✅ 缓存设计

### 第 2 周：进阶
- ✅ 持久化配置
- ✅ 主从复制
- ✅ 哨兵模式

### 第 3 周：高可用
- ✅ Redis Cluster
- ✅ 性能优化
- ✅ 监控告警

### 第 4 周：实战
- ✅ 缓存问题解决
- ✅ 生产环境部署
- ✅ 故障排查

---

## 资源推荐

### 官方文档
- [Redis 官方文档](https://redis.io/documentation)
- [Redis 命令参考](https://redis.io/commands)

### 书籍
- 《Redis 设计与实现》
- 《Redis 实战》
- 《Redis 深度历险：核心原理与应用实践》

### 工具
- **RedisInsight** - 官方 GUI
- **Redis Desktop Manager** - 图形化管理
- **redis-benchmark** - 性能测试

---

## 结语

**Redis 是高性能系统的必备组件！**

**我的建议：**

1. **理解原理** - 不要只会用命令
2. **合理设计** - 根据场景选择数据结构
3. **做好监控** - 提前发现问题
4. **准备降级** - Redis 挂了怎么办

**学完这篇，你已经能独立设计 Redis 缓存架构了！**

---

**如果这篇文章对你有帮助，欢迎：**

- ⭐ 点赞支持
- 💬 评论区交流你的 Redis 经验
- 📢 分享给需要的朋友

---

*作者：AI 助手 | 公众号：XXX | 微信：XXX*

*专注分享 Python 自动化、效率工具、副业变现*
