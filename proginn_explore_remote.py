#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 探索远程工作/整包项目页面")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问远程工作页面
    print("1️⃣ 访问远程工作页面...")
    page.goto('https://www.proginn.com/remote', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
        };
    }''')
    
    print(f"URL: {info['url']}")
    print(f"Title: {info['title'][:80]}")
    print(f"内容长度：{info['bodyLength']}")
    
    # 获取所有链接
    links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            const text = (a.innerText || '').trim();
            if (href && text) {
                result.push({href, text: text.substring(0, 80)});
            }
        });
        return result;
    }''')
    
    print(f"\n找到 {len(links)} 个链接")
    
    # 筛选项目/需求相关链接
    project_keywords = ['项目', '需求', '整包', '投标', '发布', 'bid', 'project', 'demand']
    project_links = [l for l in links if any(kw in l['href'].lower() or kw in l['text'].lower() for kw in project_keywords)]
    
    print(f"\n📦 项目相关链接 ({len(project_links)} 个):")
    for link in project_links[:30]:
        print(f"  - {link['text'][:50]} -> {link['href'][:120]}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_remote_page.png', full_page=True)
    print("\n📸 截图已保存")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
