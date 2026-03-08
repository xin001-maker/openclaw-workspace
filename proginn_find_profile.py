#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 查找正确的个人资料页面")

with open('/root/.openclaw/workspace/proginn_cookies.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问首页
    print("1️⃣ 访问首页...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 找个人中心/资料入口
    print("2️⃣ 查找个人资料入口...")
    links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a').forEach(el => {
            const text = (el.innerText || '').trim();
            const href = el.href;
            if (text && (text.includes('个人') || text.includes('资料') || text.includes('中心') || text.includes('设置') || text.includes('profile') || text.includes('center'))) {
                result.push({text, href});
            }
        });
        return result;
    }''')
    
    print(f"\n🔗 找到 {len(links)} 个相关链接:")
    for link in links[:15]:
        print(f"  - {link['text']}: {link['href'][:80]}")
    
    # 尝试访问可能的资料页面
    possible_urls = [
        'https://www.proginn.com/user/profile',
        'https://www.proginn.com/user/info',
        'https://www.proginn.com/developer/profile',
        'https://www.proginn.com/developer/resume',
    ]
    
    for url in possible_urls:
        print(f"\n3️⃣ 尝试访问：{url}")
        page.goto(url, timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        
        info = page.evaluate('''() => {
            return {
                url: window.location.href,
                title: document.title,
                has404: document.body.innerText.includes('未找到') || document.body.innerText.includes('404'),
                inputCount: document.querySelectorAll('input, textarea').length
            };
        }''')
        
        print(f"  结果：title={info['title'][:40]}, 404={info['has404']}, 输入框={info['inputCount']}")
        
        if not info['has404'] and info['inputCount'] > 0:
            print(f"  ✅ 找到有效页面！")
            page.screenshot(path='/root/.openclaw/workspace/proginn_profile_page.png', full_page=True)
            break
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
