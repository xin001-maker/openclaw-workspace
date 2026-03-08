#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 探索程序员客栈网站结构")

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
    
    # 获取所有链接
    print("2️⃣ 收集所有链接...")
    links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            const text = (a.innerText || '').trim();
            if (href && (href.includes('proginn.com'))) {
                result.push({href, text});
            }
        });
        return result;
    }''')
    
    print(f"找到 {len(links)} 个链接")
    
    # 筛选可能的项目/需求相关链接
    project_links = [l for l in links if any(kw in l['href'].lower() for kw in ['require', 'project', 'release', 'job', 'work', 'demand'])]
    
    print(f"\n📦 可能的项目相关链接 ({len(project_links)} 个):")
    for link in project_links[:20]:
        print(f"  - {link['text'][:30]} -> {link['href'][:80]}")
    
    # 尝试点击"发布需求"或类似按钮
    print("\n3️⃣ 尝试点击导航链接...")
    nav_clicks = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a, button, span[role="button"]').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && (text.includes('需求') || text.includes('项目') || text.includes('工作') || text.includes('开发'))) {
                result.push(text);
            }
        });
        return result.slice(0, 20);
    }''')
    
    print("导航元素:")
    for text in nav_clicks:
        print(f"  - {text}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_home_explore.png', full_page=True)
    print("\n📸 截图已保存")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
