#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📝 访问开发者简历页面")

with open('/root/.openclaw/workspace/proginn_cookies.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问开发者入驻/简历页面
    urls_to_try = [
        'https://www.proginn.com/developer',
        'https://www.proginn.com/developer/resume',
        'https://www.proginn.com/user/release',  # 发布需求页面，可能有项目列表
    ]
    
    for url in urls_to_try:
        print(f"\n尝试：{url}")
        page.goto(url, timeout=30000, wait_until='networkidle')
        time.sleep(3)
        
        info = page.evaluate('''() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyLength: document.body.innerText.length,
                projectCount: document.querySelectorAll('[class*="project"], [class*="release"]').length
            };
        }''')
        
        print(f"  URL: {info['url'][:60]}")
        print(f"  Title: {info['title'][:50]}")
        print(f"  文本长度：{info['bodyLength']}")
        
        page.screenshot(path=f'/root/.openclaw/workspace/proginn_{url.split("/")[-1]}.png', full_page=True)
    
    # 最后回到首页，找项目列表
    print("\n返回首页找项目列表...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    projects = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text.length > 50 && text.length < 300 && 
                (text.includes('元') || text.includes('预算') || text.includes('需求') || text.includes('开发'))) {
                result.push(text.replace(/\s+/g, ' '));
            }
        });
        return result.slice(0, 10);
    }''')
    
    print(f"\n📦 找到 {len(projects)} 个项目:")
    for i, proj in enumerate(projects[:5], 1):
        print(f"{i}. {proj[:150]}...")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
