#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 查看项目列表")

# 加载 Cookie
with open('/root/.openclaw/workspace/proginn_cookies.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问项目列表页
    print("1️⃣ 访问项目列表...")
    page.goto('https://www.proginn.com/release', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_projects.png', full_page=True)
    print("2️⃣ 已截图：proginn_projects.png")
    
    # 获取项目列表
    projects = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && text.length > 30 && text.length < 500) {
                // 检查是否包含项目特征
                if (text.includes('元') || text.includes('预算') || text.includes('需求') || 
                    text.includes('开发') || text.includes('Python') || text.includes('数据')) {
                    result.push(text);
                }
            }
        });
        return result.slice(0, 20);
    }''')
    
    print(f"\n📦 找到 {len(projects)} 个项目")
    for i, proj in enumerate(projects[:10], 1):
        print(f"\n{i}. {proj[:200]}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
