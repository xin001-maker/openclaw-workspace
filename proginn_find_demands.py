#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 查找企业发布的需求/项目列表")

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
    
    # 查找"发布需求"链接
    print("2️⃣ 查找'发布需求'链接...")
    publish_url = page.evaluate('''() => {
        let url = null;
        document.querySelectorAll('a').forEach(a => {
            const text = (a.innerText || '').trim();
            if (text.includes('发布需求') && a.href) {
                url = a.href;
            }
        });
        return url;
    }''')
    
    if publish_url:
        print(f"找到'发布需求'链接：{publish_url}")
    else:
        print("未找到'发布需求'链接")
    
    # 尝试常见的需求列表 URL
    demand_urls = [
        'https://www.proginn.com/demand',
        'https://www.proginn.com/demands',
        'https://www.proginn.com/need',
        'https://www.proginn.com/needs',
        'https://www.proginn.com/project/list',
        'https://www.proginn.com/bid',
        'https://www.proginn.com/bids',
        'https://www.proginn.com/task',
        'https://www.proginn.com/tasks',
    ]
    
    for url in demand_urls:
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
            
            if info['bodyLength'] > 3000 and '页面未找到' not in info['title']:
                print(f"  ✅ 可能是正确页面！")
                page.screenshot(path='/root/.openclaw/workspace/proginn_demand_list.png', full_page=True)
                
                # 提取项目/需求
                demands = page.evaluate('''() => {
                    const result = [];
                    document.querySelectorAll('*').forEach(el => {
                        const text = (el.innerText || '').trim();
                        if (text.length > 15 && text.length < 200) {
                            result.push(text);
                        }
                    });
                    return result;
                }''')
                
                # 筛选可能包含需求信息的文本
                demand_items = [d for d in demands if any(kw in d for kw in ['Python', '开发', '数据', '爬虫', '自动化', '工程师', '远程', '兼职', '元', '预算', '需求', '项目'])]
                
                print(f"\n找到 {len(demand_items)} 个相关需求:")
                for i, item in enumerate(demand_items[:20], 1):
                    print(f"{i}. {item[:150]}")
                
                # 保存
                with open('/root/.openclaw/workspace/proginn_demand_list.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(demands[:100]))
                print(f"\n💾 已保存内容到 proginn_demand_list.txt")
                break
        except Exception as e:
            print(f"  ❌ 错误：{e}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
