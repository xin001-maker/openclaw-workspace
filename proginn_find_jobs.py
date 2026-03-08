#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 查找岗位/项目列表")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问云端工作页面
    print("1️⃣ 访问云端工作页面...")
    page.goto('https://www.proginn.com/cloud', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 获取所有链接
    print("2️⃣ 收集所有链接...")
    links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            const text = (a.innerText || '').trim();
            if (href && href.includes('proginn.com')) {
                result.push({href, text: text.substring(0, 50)});
            }
        });
        return result;
    }''')
    
    print(f"找到 {len(links)} 个链接")
    
    # 筛选岗位/工作相关链接
    job_links = [l for l in links if any(kw in l['href'].lower() for kw in ['job', 'position', 'post', 'role', 'hire', 'apply', 'list'])]
    
    print(f"\n📦 岗位相关链接 ({len(job_links)} 个):")
    for link in job_links[:20]:
        print(f"  - {link['text']} -> {link['href'][:100]}")
    
    # 获取所有按钮和可点击元素
    print("\n3️⃣ 查找可点击元素...")
    clickable = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a, button, [role="button"], [onclick]').forEach(el => {
            const text = (el.innerText || '').trim();
            const tag = el.tagName.toLowerCase();
            if (text && text.length < 50) {
                result.push(`${tag}: ${text}`);
            }
        });
        return result;
    }''')
    
    # 筛选可能导航到岗位列表的元素
    job_elements = [e for e in clickable if any(kw in e.lower() for kw in ['岗位', '工作', '职位', '申请', '查看', '更多'])]
    
    print("可能导航到岗位列表的元素:")
    for elem in job_elements[:20]:
        print(f"  - {elem}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_cloud_page.png', full_page=True)
    print("\n📸 截图已保存")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
