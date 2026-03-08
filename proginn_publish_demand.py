#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 访问发布需求页面")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问发布需求页面
    print("1️⃣ 访问 https://www.proginn.com/type/service ...")
    page.goto('https://www.proginn.com/type/service', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_publish_demand.png', full_page=True)
    print("2️⃣ 截图已保存")
    
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
    
    # 获取所有链接
    print("\n3️⃣ 收集所有链接...")
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
    
    # 筛选可能的项目/需求列表链接
    project_links = [l for l in links if any(kw in l['href'].lower() for kw in ['list', 'project', 'demand', 'require', 'bid', 'task'])]
    
    print(f"\n📦 项目/需求相关链接 ({len(project_links)} 个):")
    for link in project_links[:20]:
        print(f"  - {link['text']} -> {link['href'][:100]}")
    
    # 提取页面主要内容
    print("\n4️⃣ 提取页面内容...")
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
    
    print("页面主要内容:")
    for i, text in enumerate(content[:30], 1):
        print(f"{i}. {text}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
