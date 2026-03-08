#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📝 检查开发者入驻流程")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
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
    
    # 查找"开发者入驻"链接
    print("2️⃣ 查找'开发者入驻'链接...")
    join_url = page.evaluate('''() => {
        let url = null;
        document.querySelectorAll('a').forEach(a => {
            const text = (a.innerText || '').trim();
            if (text.includes('开发者入驻') && a.href) {
                url = a.href;
            }
        });
        return url;
    }''')
    
    if join_url:
        print(f"找到'开发者入驻'链接：{join_url}")
        page.goto(join_url, timeout=60000, wait_until='networkidle')
        time.sleep(5)
    else:
        # 尝试常见 URL
        print("未找到链接，尝试常见 URL...")
        page.goto('https://www.proginn.com/join', timeout=60000, wait_until='networkidle')
        time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_join_developer.png', full_page=True)
    print("3️⃣ 截图已保存")
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
        };
    }''')
    
    print(f"\n📄 URL: {info['url'][:100]}")
    print(f"📄 Title: {info['title'][:60]}")
    print(f"📄 内容长度：{info['bodyLength']}")
    
    # 提取页面内容
    print("\n4️⃣ 提取页面内容...")
    content = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text.length > 15 && text.length < 250) {
                result.push(text);
            }
        });
        return result.slice(0, 40);
    }''')
    
    print("页面主要内容:")
    for i, text in enumerate(content[:25], 1):
        print(f"{i}. {text}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
