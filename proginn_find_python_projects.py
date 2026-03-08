#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🎯 查找 Python 相关项目")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问后端开发分类（Python 属于后端）
    categories = [
        'https://www.proginn.com/cat/houd',  # 后端
        'https://www.proginn.com/cat/python',  # Python
        'https://www.proginn.com/cat/all',  # 全部
    ]
    
    found_projects = []
    
    for url in categories:
        print(f"\n{'='*60}")
        print(f"尝试：{url}")
        print('='*60)
        
        try:
            page.goto(url, timeout=60000, wait_until='networkidle')
            time.sleep(5)
            
            info = page.evaluate('''() => {
                return {
                    url: window.location.href,
                    title: document.title,
                    bodyLength: document.body.innerText.length,
                };
            }''')
            
            print(f"Title: {info['title'][:60]}")
            print(f"内容长度：{info['bodyLength']}")
            
            if info['bodyLength'] < 1000:
                print("⚠️ 内容太少，跳过")
                continue
            
            # 提取所有项目链接
            projects = page.evaluate('''() => {
                const result = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.href;
                    const text = (a.innerText || '').trim();
                    // 匹配 /w/ 开头的链接（项目）
                    if (href && href.includes('/w/')) {
                        result.push({href, text: text.substring(0, 150)});
                    }
                });
                return result;
            }''')
            
            if projects:
                print(f"\n找到 {len(projects)} 个项目链接:")
                for proj in projects[:20]:
                    print(f"  - {proj['text'][:80]}")
                    print(f"    -> {proj['href']}")
                    found_projects.append(proj)
            
        except Exception as e:
            print(f"❌ 错误：{e}")
    
    print(f"\n{'='*60}")
    print(f"总共找到 {len(found_projects)} 个项目")
    print('='*60)
    
    # 保存项目列表
    if found_projects:
        with open('/root/.openclaw/workspace/proginn_found_projects.json', 'w', encoding='utf-8') as f:
            json.dump(found_projects, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存到 proginn_found_projects.json")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
