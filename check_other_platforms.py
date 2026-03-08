#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 探索其他外包平台")

platforms = {
    "码市": "https://codemart.com",
    "开源众包": "https://zb.oschina.net",
    "实现网": "https://shixian.com",
    "猪八戒": "https://www.zbj.com",
}

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    results = []
    
    for name, url in platforms.items():
        print(f"\n{'='*50}")
        print(f"尝试：{name} - {url}")
        print('='*50)
        
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
            
            print(f"✅ 可访问")
            print(f"   Title: {info['title'][:50]}")
            print(f"   内容长度：{info['bodyLength']}")
            
            # 查找项目/需求相关关键词
            has_projects = page.evaluate('''() => {
                const text = document.body.innerText;
                return text.includes('项目') || text.includes('需求') || text.includes('外包') || text.includes('投标');
            }''')
            
            results.append({
                "name": name,
                "url": url,
                "accessible": True,
                "title": info['title'][:50],
                "has_projects": has_projects,
                "content_length": info['bodyLength']
            })
            
        except Exception as e:
            print(f"❌ 无法访问：{e}")
            results.append({
                "name": name,
                "url": url,
                "accessible": False,
                "error": str(e)[:100]
            })
    
    browser.close()
    
    # 保存结果
    print("\n" + "="*50)
    print("📊 平台可访问性总结")
    print("="*50)
    
    accessible = [r for r in results if r.get('accessible')]
    print(f"\n✅ 可访问平台 ({len(accessible)} 个):")
    for r in accessible:
        project_flag = "📦 有项目" if r.get('has_projects') else ""
        print(f"   - {r['name']}: {r['url']} {project_flag}")
    
    inaccessible = [r for r in results if not r.get('accessible')]
    if inaccessible:
        print(f"\n❌ 无法访问平台 ({len(inaccessible)} 个):")
        for r in inaccessible:
            print(f"   - {r['name']}: {r.get('error', '未知错误')}")
    
    # 保存结果到文件
    with open('/root/.openclaw/workspace/platform_check.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 结果已保存到 platform_check.json")
    
except Exception as e:
    print(f"❌ 错误：{e}")
