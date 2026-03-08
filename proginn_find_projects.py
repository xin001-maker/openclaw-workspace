#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"
PASSWORD = "J.o123456"

print("🔍 查找真实项目列表")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    # 登录
    print("1️⃣ 登录...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(3)
    page.evaluate(f'''() => {{
        document.querySelectorAll('*').forEach(el => {{
            if ((el.innerText || '').trim() === '登录') el.click();
        }});
        setTimeout(() => {{
            document.querySelectorAll('input').forEach(input => {{
                const placeholder = (input.placeholder || '').toLowerCase();
                if (placeholder.includes('手机') || placeholder.includes('账号')) input.value = "{PHONE}";
                if (input.type === 'password') input.value = "{PASSWORD}";
            }});
            document.querySelectorAll('*').forEach(el => {{
                const text = (el.innerText || '').trim();
                if (text.includes('登录') && text.length < 10) el.click();
            }});
        }}, 2000);
    }}''')
    time.sleep(8)
    
    # 尝试多个项目列表 URL
    urls = [
        'https://www.proginn.com/requirement/list',
        'https://www.proginn.com/developer/requirement',
        'https://www.proginn.com/b/release',
    ]
    
    for url in urls:
        print(f"\n尝试：{url}")
        page.goto(url, timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        
        info = page.evaluate('''() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyLength: document.body.innerText.length
            };
        }''')
        
        print(f"  Title: {info['title'][:40]}, 内容：{info['bodyLength']} 字符")
        
        if info['bodyLength'] > 5000:
            print("  ✅ 可能是正确页面！")
            page.screenshot(path='/root/.openclaw/workspace/proginn_project_list.png', full_page=True)
            
            # 提取项目
            projects = page.evaluate('''() => {
                const result = [];
                document.querySelectorAll('[class*="require"], [class*="project"], [class*="release"]').forEach(el => {
                    const text = (el.innerText || '').trim();
                    if (text.length > 20 && text.length < 300) {
                        result.push(text);
                    }
                });
                return result.slice(0, 10);
            }''')
            
            if projects:
                print(f"\n📦 找到 {len(projects)} 个项目:")
                for i, p in enumerate(projects[:5], 1):
                    print(f"{i}. {p[:150]}")
            break
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
