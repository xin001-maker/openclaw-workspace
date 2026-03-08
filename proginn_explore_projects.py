#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 探索项目发布/整包开发页面")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 尝试访问整包开发页面
    urls = [
        'https://www.proginn.com/b/outsource',
        'https://www.proginn.com/b/p1980',
        'https://www.proginn.com/type/service',
        'https://www.proginn.com/cat/xmjl',
    ]
    
    for url in urls:
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
            
            print(f"URL: {info['url'][:100]}")
            print(f"Title: {info['title'][:80]}")
            print(f"内容长度：{info['bodyLength']}")
            
            # 获取所有链接
            links = page.evaluate('''() => {
                const result = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.href;
                    const text = (a.innerText || '').trim();
                    if (href && text && text.length < 100) {
                        result.push({href, text});
                    }
                });
                return result;
            }''')
            
            # 筛选项目相关
            project_keywords = ['项目', '需求', '整包', '投标', '发布', 'list', 'project', 'demand', 'bid']
            project_links = [l for l in links if any(kw in l['href'].lower() or kw in l['text'].lower() for kw in project_keywords)]
            
            if project_links:
                print(f"\n📦 项目相关链接 ({len(project_links)} 个):")
                for link in project_links[:20]:
                    print(f"  - {link['text'][:50]} -> {link['href'][:100]}")
            
            # 截图
            filename = url.replace('https://www.proginn.com/', '').replace('/', '_').replace('?', '_') + '.png'
            page.screenshot(path=f'/root/.openclaw/workspace/proginn_explore_{filename}.png', full_page=True)
            print(f"\n📸 截图已保存：proginn_explore_{filename}")
            
            # 如果内容长度合理，提取文本
            if info['bodyLength'] > 2000:
                content = page.evaluate('''() => {
                    const items = [];
                    document.querySelectorAll('*').forEach(el => {
                        const text = (el.innerText || '').trim();
                        if (text.length > 30 && text.length < 200) {
                            items.push(text);
                        }
                    });
                    return items.slice(0, 30);
                }''')
                
                print("\n页面内容片段:")
                for i, text in enumerate(content[:15], 1):
                    if any(kw in text for kw in ['Python', '开发', '数据', '爬虫', '自动化', '元', '预算', '急']):
                        print(f"{i}. {text[:150]}")
                
        except Exception as e:
            print(f"❌ 错误：{e}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
