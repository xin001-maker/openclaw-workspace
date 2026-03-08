#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 查找开发者投标项目列表")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 尝试开发者相关的 URL
    developer_urls = [
        'https://www.proginn.com/developer',
        'https://www.proginn.com/developercenter',
        'https://www.proginn.com/developer/center',
        'https://www.proginn.com/developer/home',
        'https://www.proginn.com/developer/dashboard',
        'https://www.proginn.com/developer/projects',
        'https://www.proginn.com/developer/bid',
        'https://www.proginn.com/developerCenter',
        'https://www.proginn.com/user/center',
        'https://www.proginn.com/my',
    ]
    
    for url in developer_urls:
        print(f"\n尝试：{url}")
        try:
            page.goto(url, timeout=30000, wait_until='domcontentloaded')
            time.sleep(3)
            
            info = page.evaluate('''() => {
                return {
                    url: window.location.href,
                    title: document.title,
                    bodyLength: document.body.innerText.length,
                };
            }''')
            
            print(f"  Title: {info['title'][:50]}")
            print(f"  内容长度：{info['bodyLength']}")
            
            if info['bodyLength'] > 2000 and '页面未找到' not in info['title'] and '登录' not in info['title']:
                print(f"  ✅ 可能是正确页面！")
                page.screenshot(path='/root/.openclaw/workspace/proginn_developer_center.png', full_page=True)
                
                # 提取内容
                content = page.evaluate('''() => {
                    const result = [];
                    document.querySelectorAll('*').forEach(el => {
                        const text = (el.innerText || '').trim();
                        if (text.length > 15 && text.length < 200) {
                            result.push(text);
                        }
                    });
                    return result.slice(0, 50);
                }''')
                
                print("\n页面内容:")
                for i, text in enumerate(content[:30], 1):
                    if any(kw in text for kw in ['项目', '需求', '投标', 'Python', '开发', '数据', '爬虫']):
                        print(f"{i}. {text[:150]}")
                
                break
        except Exception as e:
            print(f"  ❌ 错误：{e}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
