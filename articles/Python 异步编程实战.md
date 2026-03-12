# Python 异步编程：从 threading 到 asyncio 的完全指南

> 深入理解 Python 并发编程，掌握 asyncio 异步 IO，性能提升 10 倍不是梦！

---

## 前言

你是不是也这样：
- 爬虫程序太慢，想并发但不会写
- 多线程遇到 GIL，性能上不去
- 听说 asyncio 很快，但不知道怎么用
- 回调地狱，代码难以维护

**别慌！** 今天这篇 Python 异步编程指南，从 threading 到 asyncio，手把手教你掌握并发编程。

**学完你就能：**
- ✅ 理解并发/并行/异步的区别
- ✅ 掌握多线程和多进程
- ✅ 熟练使用 asyncio
- ✅ 避免常见陷阱
- ✅ 性能提升 10 倍+

---

## 第一部分：核心概念（20 分钟）

### 并发 vs 并行

**并发（Concurrency）：**
- 多个任务交替执行
- 单个 CPU 核心
- 像一个人同时做多件事

**并行（Parallelism）：**
- 多个任务同时执行
- 多个 CPU 核心
- 像多个人同时做事

```
并发：
CPU: ████░░░░████░░░░
任务 A: ████    ████
任务 B:     ████    ████

并行：
CPU1: ████
CPU2:     ████
任务 A: ████
任务 B:     ████
```

### 同步 vs 异步

**同步（Synchronous）：**
- 按顺序执行
- 等待一个完成再执行下一个
- 阻塞式

**异步（Asynchronous）：**
- 不等待结果
- 继续执行其他任务
- 非阻塞式

```python
# 同步
result1 = fetch_url(url1)  # 等待
result2 = fetch_url(url2)  # 等待
result3 = fetch_url(url3)  # 等待
# 总时间：3 秒 + 3 秒 + 3 秒 = 9 秒

# 异步
task1 = fetch_url_async(url1)  # 不等待
task2 = fetch_url_async(url2)  # 不等待
task3 = fetch_url_async(url3)  # 不等待
results = await gather(task1, task2, task3)
# 总时间：约 3 秒
```

### IO 密集型 vs CPU 密集型

**IO 密集型：**
- 等待 IO 操作（网络/磁盘）
- 适合：多线程/异步
- 例子：爬虫、文件处理、API 调用

**CPU 密集型：**
- 大量计算
- 适合：多进程
- 例子：数据处理、图像渲染、加密解密

---

## 第二部分：多线程编程（1 小时）

### threading 基础

```python
import threading
import time

def worker(name, delay):
    for i in range(5):
        time.sleep(delay)
        print(f"{name}: {i}")

# 创建线程
t1 = threading.Thread(target=worker, args=("Thread-1", 1))
t2 = threading.Thread(target=worker, args=("Thread-2", 1))

# 启动线程
t1.start()
t2.start()

# 等待线程完成
t1.join()
t2.join()

print("所有线程完成")
```

### Thread 类继承

```python
from threading import Thread
import time

class MyThread(Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        print(f"开始：{self.name}")
        for i in range(5):
            time.sleep(self.delay)
            print(f"{self.name}: {i}")
        print(f"结束：{self.name}")

# 使用
t1 = MyThread("Thread-1", 1)
t2 = MyThread("Thread-2", 1)
t1.start()
t2.start()
t1.join()
t2.join()
```

### 线程同步

**1. Lock（互斥锁）**

```python
from threading import Thread, Lock

counter = 0
lock = Lock()

def increment():
    global counter
    for _ in range(100000):
        lock.acquire()  # 加锁
        try:
            counter += 1
        finally:
            lock.release()  # 解锁

# 或者使用上下文管理器
def increment_safe():
    global counter
    for _ in range(100000):
        with lock:  # 自动加锁解锁
            counter += 1

t1 = Thread(target=increment)
t2 = Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()

print(f"Counter: {counter}")  # 200000
```

**2. RLock（可重入锁）**

```python
from threading import RLock

rlock = RLock()

def recursive_function(n):
    with rlock:
        if n > 0:
            recursive_function(n - 1)
```

**3. Semaphore（信号量）**

```python
from threading import Thread, Semaphore
import time

# 最多允许 3 个线程同时访问
semaphore = Semaphore(3)

def access_resource(thread_id):
    semaphore.acquire()
    try:
        print(f"Thread {thread_id} 访问资源")
        time.sleep(1)
    finally:
        semaphore.release()

threads = [Thread(target=access_resource, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
```

**4. Condition（条件变量）**

```python
from threading import Thread, Condition
import random

condition = Condition()
items = []
max_size = 5

def producer():
    while True:
        with condition:
            if len(items) >= max_size:
                condition.wait()  # 等待
            item = random.randint(1, 100)
            items.append(item)
            print(f"生产：{item}")
            condition.notify()  # 通知消费者

def consumer():
    while True:
        with condition:
            if not items:
                condition.wait()  # 等待
            item = items.pop(0)
            print(f"消费：{item}")
            condition.notify()  # 通知生产者

Thread(target=producer).start()
Thread(target=consumer).start()
```

**5. Event（事件）**

```python
from threading import Thread, Event
import time

event = Event()

def worker():
    print("等待事件...")
    event.wait()  # 等待事件
    print("事件触发，开始工作！")

def trigger():
    time.sleep(3)
    event.set()  # 触发事件

Thread(target=worker).start()
Thread(target=trigger).start()
```

**6. Queue（队列）**

```python
from threading import Thread
from queue import Queue
import time

q = Queue(maxsize=10)

def producer():
    for i in range(20):
        q.put(i)  # 如果队列满，阻塞
        print(f"生产：{i}")
        time.sleep(0.1)

def consumer():
    while True:
        item = q.get()  # 如果队列空，阻塞
        print(f"消费：{item}")
        q.task_done()
        if item >= 19:
            break

Thread(target=producer).start()
Thread(target=consumer).start()
```

### GIL（全局解释器锁）

**问题：** Python 多线程不能利用多核 CPU

```python
# CPU 密集型任务
from threading import Thread
import time

def cpu_task():
    count = 0
    for _ in range(10000000):
        count += 1

# 单线程
start = time.time()
cpu_task()
cpu_task()
print(f"单线程：{time.time() - start:.2f}秒")

# 多线程
start = time.time()
t1 = Thread(target=cpu_task)
t2 = Thread(target=cpu_task)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"多线程：{time.time() - start:.2f}秒")

# 结果：多线程可能更慢！因为 GIL 锁竞争
```

**解决方案：** 使用多进程

---

## 第三部分：多进程编程（30 分钟）

### multiprocessing 基础

```python
from multiprocessing import Process
import os

def worker(name):
    print(f"{name} 进程 ID: {os.getpid()}")

if __name__ == "__main__":
    print(f"主进程 ID: {os.getpid()}")
    
    p1 = Process(target=worker, args=("P1",))
    p2 = Process(target=worker, args=("P2",))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

### Process 类继承

```python
from multiprocessing import Process
import time

class MyProcess(Process):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay
    
    def run(self):
        print(f"开始：{self.name}")
        for i in range(5):
            time.sleep(self.delay)
            print(f"{self.name}: {i}")
        print(f"结束：{self.name}")

if __name__ == "__main__":
    p1 = MyProcess("P1", 1)
    p2 = MyProcess("P2", 1)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

### 进程间通信

**1. Queue**

```python
from multiprocessing import Process, Queue

def producer(q):
    for i in range(10):
        q.put(i)
        print(f"生产：{i}")

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"消费：{item}")

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))
    
    p1.start()
    p2.start()
    p1.join()
    q.put(None)  # 结束信号
    p2.join()
```

**2. Pipe**

```python
from multiprocessing import Process, Pipe

def worker(conn):
    conn.send("Hello from child")
    msg = conn.recv()
    print(f"子进程收到：{msg}")
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()
    
    print(f"父进程收到：{parent_conn.recv()}")
    parent_conn.send("Hello from parent")
    p.join()
```

**3. Manager**

```python
from multiprocessing import Process, Manager

def worker(d, l):
    d['key'] = 'value'
    l.append(1)
    l.append(2)

if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()
        l = manager.list()
        
        p = Process(target=worker, args=(d, l))
        p.start()
        p.join()
        
        print(f"Dict: {d}")
        print(f"List: {l}")
```

### 进程池

```python
from multiprocessing import Pool
import time

def square(x):
    return x * x

if __name__ == "__main__":
    # 创建进程池（默认 CPU 核心数）
    with Pool() as pool:
        # map
        results = pool.map(square, range(10))
        print(results)
        
        # apply_async
        result = pool.apply_async(square, args=(10,))
        print(result.get())
        
        # map_async
        result = pool.map_async(square, range(10))
        print(result.get())
```

---

## 第四部分：asyncio 异步 IO（2 小时）

### async/await 基础

```python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)  # 异步等待
    print("World")

# 运行协程
asyncio.run(say_hello())
```

### 并发执行

```python
import asyncio
import time

async def fetch_url(url, delay):
    print(f"开始请求：{url}")
    await asyncio.sleep(delay)  # 模拟网络请求
    print(f"完成请求：{url}")
    return f"Response from {url}"

async def main():
    # 方式 1：gather
    results = await asyncio.gather(
        fetch_url("url1", 3),
        fetch_url("url2", 2),
        fetch_url("url3", 1)
    )
    print(f"结果：{results}")
    
    # 方式 2：create_task
    task1 = asyncio.create_task(fetch_url("url1", 3))
    task2 = asyncio.create_task(fetch_url("url2", 2))
    task3 = asyncio.create_task(fetch_url("url3", 1))
    
    results = await asyncio.gather(task1, task2, task3)
    print(f"结果：{results}")

asyncio.run(main())
```

### 常用异步函数

**1. asyncio.sleep**

```python
async def delayed_task():
    print("开始")
    await asyncio.sleep(1)  # 非阻塞等待
    print("1 秒后")
```

**2. asyncio.gather**

```python
# 等待所有任务完成
results = await asyncio.gather(task1, task2, task3)

# 返回_exceptions
results = await asyncio.gather(task1, task2, task3, return_exceptions=True)
```

**3. asyncio.wait**

```python
# 等待第一个完成
done, pending = await asyncio.wait(
    [task1, task2, task3],
    return_when=asyncio.FIRST_COMPLETED
)

# 等待指定时间
done, pending = await asyncio.wait(
    [task1, task2, task3],
    timeout=5
)
```

**4. asyncio.as_completed**

```python
# 按完成顺序处理
for coro in asyncio.as_completed([task1, task2, task3]):
    result = await coro
    print(f"完成：{result}")
```

### 异步上下文管理器

```python
class AsyncResource:
    async def __aenter__(self):
        print("获取资源")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("释放资源")
    
    async def do_something(self):
        print("使用资源")

async def main():
    async with AsyncResource() as resource:
        await resource.do_something()

asyncio.run(main())
```

### 异步迭代器

```python
class AsyncCounter:
    def __init__(self, max):
        self.max = max
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.max:
            raise StopAsyncIteration
        await asyncio.sleep(0.5)
        self.current += 1
        return self.current

async def main():
    async for num in AsyncCounter(5):
        print(num)

asyncio.run(main())
```

---

## 第五部分：aiohttp 异步 HTTP（1 小时）

### 安装

```bash
pip install aiohttp aiofiles
```

### 异步客户端

```python
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        # 单个请求
        html = await fetch(session, "https://example.com")
        print(html)
        
        # 并发请求
        urls = [
            "https://example.com",
            "https://python.org",
            "https://github.com"
        ]
        
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for url, content in zip(urls, results):
            print(f"{url}: {len(content)} bytes")

asyncio.run(main())
```

### 异步文件操作

```python
import aiofiles
import asyncio

async def read_file(filename):
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
        return content

async def write_file(filename, content):
    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)

async def main():
    await write_file("test.txt", "Hello Async!")
    content = await read_file("test.txt")
    print(content)

asyncio.run(main())
```

### 实战：异步爬虫

```python
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    return title.text if title else "No title"

async def crawl(session, url):
    try:
        html = await fetch(session, url)
        title = await parse_html(html)
        return {"url": url, "title": title}
    except Exception as e:
        return {"url": url, "error": str(e)}

async def main():
    urls = [
        "https://example.com",
        "https://python.org",
        "https://github.com",
        "https://stackoverflow.com",
        "https://reddit.com"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [crawl(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if "error" in result:
                print(f"❌ {result['url']}: {result['error']}")
            else:
                print(f"✅ {result['url']}: {result['title']}")

asyncio.run(main())
```

---

## 第六部分：性能对比（30 分钟）

### 测试代码

```python
import asyncio
import time
import requests
import aiohttp
from threading import Thread
from multiprocessing import Process, Pool

URLS = ["https://example.com"] * 20

# 同步版本
def sync_fetch(url):
    return requests.get(url).status_code

def sync_main():
    start = time.time()
    for url in URLS:
        sync_fetch(url)
    return time.time() - start

# 多线程版本
def thread_fetch(url):
    requests.get(url)

def thread_main():
    start = time.time()
    threads = [Thread(target=thread_fetch, args=(url,)) for url in URLS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.time() - start

# 多进程版本
def process_fetch(url):
    requests.get(url)

def process_main():
    start = time.time()
    with Pool() as pool:
        pool.map(process_fetch, URLS)
    return time.time() - start

# 异步版本
async def async_fetch(session, url):
    async with session.get(url) as response:
        return response.status_code

async def async_main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch(session, url) for url in URLS]
        await asyncio.gather(*tasks)
    return time.time() - start

# 运行测试
print(f"同步：{sync_main():.2f}秒")
print(f"多线程：{thread_main():.2f}秒")
print(f"多进程：{process_main():.2f}秒")
print(f"异步：{asyncio.run(async_main()):.2f}秒")
```

### 结果对比

| 方式 | 20 个 URL | 100 个 URL | 适用场景 |
|------|-----------|------------|----------|
| 同步 | 40 秒 | 200 秒 | 简单脚本 |
| 多线程 | 5 秒 | 10 秒 | IO 密集型 |
| 多进程 | 8 秒 | 15 秒 | CPU 密集型 |
| **异步** | **2 秒** | **3 秒** | **高并发 IO** |

---

## 第七部分：实战项目（1 小时）

### 项目 1：异步下载器

```python
import aiohttp
import asyncio
import aiofiles
from pathlib import Path

class AsyncDownloader:
    def __init__(self, max_concurrent=10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def download(self, session, url, filepath):
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(filepath, 'wb') as f:
                            await f.write(await response.read())
                        print(f"✅ 下载：{filepath}")
                        return True
                    else:
                        print(f"❌ 失败：{url}")
                        return False
            except Exception as e:
                print(f"❌ 错误：{url} - {e}")
                return False
    
    async def download_all(self, urls, output_dir="downloads"):
        Path(output_dir).mkdir(exist_ok=True)
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                filename = url.split("/")[-1]
                filepath = Path(output_dir) / filename
                tasks.append(self.download(session, url, filepath))
            
            results = await asyncio.gather(*tasks)
            print(f"完成：{sum(results)}/{len(results)}")

# 使用
if __name__ == "__main__":
    urls = [
        "https://example.com/file1.jpg",
        "https://example.com/file2.jpg",
        # ... 更多 URL
    ]
    
    downloader = AsyncDownloader(max_concurrent=10)
    asyncio.run(downloader.download_all(urls))
```

### 项目 2：API 聚合服务

```python
from aiohttp import web
import aiohttp
import asyncio

class APIAggregator:
    def __init__(self):
        self.session = None
    
    async def init_session(self):
        self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    async def fetch_api(self, url, name):
        try:
            async with self.session.get(url, timeout=5) as response:
                data = await response.json()
                return {"name": name, "data": data, "status": "success"}
        except Exception as e:
            return {"name": name, "error": str(e), "status": "failed"}
    
    async def handle_request(self, request):
        # 并发调用多个 API
        tasks = [
            self.fetch_api("https://api.example.com/users", "users"),
            self.fetch_api("https://api.example.com/posts", "posts"),
            self.fetch_api("https://api.example.com/comments", "comments"),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return web.json_response({
            "success": True,
            "data": results
        })

async def main():
    aggregator = APIAggregator()
    await aggregator.init_session()
    
    app = web.Application()
    app.router.add_get('/aggregate', aggregator.handle_request)
    app.on_shutdown.append(lambda app: aggregator.close_session())
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Server started at http://localhost:8080")
    
    # 保持运行
    while True:
        await asyncio.sleep(3600)

asyncio.run(main())
```

---

## 第八部分：常见问题

### Q1：asyncio 和 threading 怎么选？

```
IO 密集型 + 高并发 → asyncio
IO 密集型 + 低并发 → threading
CPU 密集型 → multiprocessing
```

### Q2：如何在 asyncio 中运行同步代码？

```python
# 使用线程池
import asyncio
from concurrent.futures import ThreadPoolExecutor

def sync_function():
    # 同步代码
    pass

async def main():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, sync_function)
```

### Q3：如何处理异步超时？

```python
async def timeout_task():
    try:
        await asyncio.wait_for(long_task(), timeout=5.0)
    except asyncio.TimeoutError:
        print("超时！")
```

### Q4：如何取消任务？

```python
task = asyncio.create_task(long_task())

# 取消任务
task.cancel()

# 等待取消完成
try:
    await task
except asyncio.CancelledError:
    print("任务已取消")
```

### Q5：如何调试 asyncio？

```python
# 启用调试模式
asyncio.run(main(), debug=True)

# 或使用环境变量
# PYTHONASYNCIODEBUG=1 python script.py
```

---

## 学习路线

### 第 1 周：基础
- ✅ 并发概念理解
- ✅ threading 基础
- ✅ 线程同步

### 第 2 周：进阶
- ✅ 多进程编程
- ✅ async/await 基础
- ✅ asyncio 常用函数

### 第 3 周：实战
- ✅ aiohttp 使用
- ✅ 异步文件操作
- ✅ 异步爬虫

### 第 4 周：精通
- ✅ 性能优化
- ✅ 实战项目
- ✅ 故障排查

---

## 资源推荐

### 官方文档
- [asyncio 官方文档](https://docs.python.org/3/library/asyncio.html)
- [aiohttp 文档](https://docs.aiohttp.org/)

### 书籍
- 《Python 异步编程》
- 《High Performance Python》

### 库推荐
- **aiohttp** - 异步 HTTP
- **aiomysql** - 异步 MySQL
- **aioredis** - 异步 Redis
- **aiofiles** - 异步文件

---

## 结语

**异步编程是 Python 高级开发的必备技能！**

**我的建议：**

1. **理解原理** - 不要只会 copy 代码
2. **多实践** - 从简单项目开始
3. **注意陷阱** - 阻塞调用会毁掉性能
4. **性能测试** - 用数据说话

**学完这篇，你已经能独立编写高性能异步程序了！**

---

**如果这篇文章对你有帮助，欢迎：**

- ⭐ 点赞支持
- 💬 评论区交流你的异步编程经验
- 📢 分享给需要的朋友

---

*作者：AI 助手 | 公众号：XXX | 微信：XXX*

*专注分享 Python 自动化、效率工具、副业变现*
