#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 访问项目列表页面")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 尝试多个项目列表 URL
    urls = [
        'https://www.proginn.com/requirement',
        'https://www.proginn.com/requirements',
        'https://www.proginn.com/project',
        'https://www.proginn.com/projects',
        'https://www.proginn.com/release/list',
    ]
    
    for url in urls:
        print(f"\n尝试：{url}")
        page.goto(url, timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        
        info = page.evaluate('''() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyLength: document.body.innerText.length,
            };
        }''')
        
        print(f"  Title: {info['title'][:40]}, 内容长度：{info['bodyLength']}")
        
        if info['bodyLength'] > 2000:
            print(f"  ✅ 可能是正确页面！")
            page.screenshot(path='/root/.openclaw/workspace/proginn_project_list.png', full_page=True)
            
            # 提取项目
            projects = page.evaluate('''() => {
                const result = [];
                document.querySelectorAll('*').forEach(el => {
                    const text = (el.innerText || '').trim();
                    if (text.length > 20 && text.length < 300) {
                        result.push(text);
                    }
                });
                return result.slice(0, 20);
            }''')
            
            print(f"\n找到 {len(projects)} 个内容块:")
            for i, text in enumerate(projects[:10], 1):
                if any(kw in text for kw in ['Python', '开发', '数据', '爬虫', '自动化', '元', '预算']):
                    print(f"{i}. {text[:150]}")
            break
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
