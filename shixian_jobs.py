#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 查看实现网兼职需求")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    # 访问兼职需求页面
    print("1️⃣ 访问兼职需求页面...")
    page.goto('https://shixian.com/jobs', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/shixian_jobs.png', full_page=True)
    print("2️⃣ 截图已保存")
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
        };
    }''')
    
    print(f"\n📄 URL: {info['url'][:80]}")
    print(f"📄 Title: {info['title'][:60]}")
    print(f"📄 内容长度：{info['bodyLength']}")
    
    # 提取需求列表
    print("\n3️⃣ 提取需求列表...")
    jobs = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text.length > 10 && text.length < 300) {
                result.push(text);
            }
        });
        return result;
    }''')
    
    # 筛选可能包含需求信息的文本
    print(f"共提取 {len(jobs)} 条内容")
    
    # 找需求项目
    job_items = []
    for j in jobs:
        if any(kw in j for kw in ['招聘', '需求', '工程师', '开发', 'Python', '前端', '后端', '全栈', '远程', '兼职', '元/天', '元/月']):
            if j not in job_items and len(j) > 15:
                job_items.append(j)
    
    print(f"\n找到 {len(job_items)} 个相关需求:")
    for i, item in enumerate(job_items[:25], 1):
        print(f"{i}. {item[:150]}")
    
    # 保存结果
    with open('/root/.openclaw/workspace/shixian_jobs.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(job_items[:50]))
    print(f"\n💾 已保存前 50 条到 shixian_jobs.txt")
    
    browser.close()
    
    print("\n✅ 探索完成")
    
except Exception as e:
    print(f"❌ 错误：{e}")
