#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🎯 查找可投标的项目列表（整包项目）")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问云端工作页面
    print("1️⃣ 访问云端工作页面...")
    page.goto('https://www.proginn.com/cloud', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 查找"整包项目"标签/链接
    print("2️⃣ 查找'整包项目'链接...")
    project_url = page.evaluate('''() => {
        let url = null;
        document.querySelectorAll('a').forEach(a => {
            const text = (a.innerText || '').trim();
            const href = a.href || '';
            if (text.includes('整包项目') && href) {
                url = href;
            }
            // 也查找包含"项目"、"需求"的链接
            if ((text.includes('项目') || text.includes('需求')) && href && !url) {
                if (href.includes('project') || href.includes('demand') || href.includes('bid')) {
                    url = href;
                }
            }
        });
        return url;
    }''')
    
    if project_url:
        print(f"找到'整包项目'链接：{project_url}")
        page.goto(project_url, timeout=60000, wait_until='networkidle')
        time.sleep(5)
    else:
        # 尝试常见的项目列表 URL
        project_urls = [
            'https://www.proginn.com/project',
            'https://www.proginn.com/projects',
            'https://www.proginn.com/bid',
            'https://www.proginn.com/bids',
            'https://www.proginn.com/demand',
            'https://www.proginn.com/demands',
            'https://www.proginn.com/zb',  # 整包缩写
            'https://www.proginn.com/cloud/project',
        ]
        
        for url in project_urls:
            print(f"尝试：{url}")
            try:
                page.goto(url, timeout=30000, wait_until='domcontentloaded')
                time.sleep(3)
                
                title = page.title()
                if '页面未找到' not in title and len(page.content()) > 5000:
                    print(f"  ✅ 成功：{title[:50]}")
                    break
            except:
                pass
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_projects_list.png', full_page=True)
    print("3️⃣ 截图已保存")
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
        };
    }''')
    
    print(f"\n📄 URL: {info['url']}")
    print(f"📄 Title: {info['title'][:80]}")
    print(f"📄 内容长度：{info['bodyLength']}")
    
    # 提取项目列表
    print("\n4️⃣ 提取项目...")
    items = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text.length > 20 && text.length < 300) {
                result.push(text);
            }
        });
        return result;
    }''')
    
    # 筛选可能包含项目信息的文本
    project_keywords = ['Python', '开发', '数据', '爬虫', '自动化', '系统', '网站', '小程序', 'APP', '预算', '元', '需求', '项目', '急', '招']
    project_items = [p for p in items if any(kw in p for kw in project_keywords)]
    
    print(f"\n找到 {len(project_items)} 个相关项目:")
    for i, item in enumerate(project_items[:30], 1):
        print(f"{i}. {item[:200]}")
    
    # 保存
    with open('/root/.openclaw/workspace/proginn_projects.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(project_items[:50]))
    print(f"\n💾 已保存前 50 个项目到 proginn_projects.txt")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
