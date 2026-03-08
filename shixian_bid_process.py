#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 探索实现网投标流程")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    # 访问兼职需求页面
    print("1️⃣ 访问兼职需求页面...")
    page.goto('https://shixian.com/jobs', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 查找具体的项目链接
    print("2️⃣ 查找项目列表...")
    project_links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            const text = (a.innerText || '').trim();
            // 查找项目详情页链接
            if (href && href.includes('/jobs/') && text.length > 10) {
                result.push({href, text: text.substring(0, 80)});
            }
        });
        return result.slice(0, 20);
    }''')
    
    print(f"找到 {len(project_links)} 个项目链接:")
    for link in project_links[:10]:
        print(f"  - {link['text']} -> {link['href'][:100]}")
    
    # 访问第一个项目详情
    if project_links:
        print(f"\n3️⃣ 访问项目详情：{project_links[0]['href']}")
        page.goto(project_links[0]['href'], timeout=60000, wait_until='networkidle')
        time.sleep(5)
        
        # 截图
        page.screenshot(path='/root/.openclaw/workspace/shixian_project_detail.png', full_page=True)
        print("4️⃣ 截图已保存")
        
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
        
        # 查找投标/申请按钮
        print("\n5️⃣ 查找投标/申请按钮...")
        apply_buttons = page.evaluate('''() => {
            const result = [];
            document.querySelectorAll('a, button, [role="button"]').forEach(el => {
                const text = (el.innerText || '').trim();
                const tag = el.tagName.toLowerCase();
                if (text && (text.includes('申请') || text.includes('投标') || text.includes('联系') || text.includes('报名'))) {
                    result.push(`${tag}: ${text}`);
                }
            });
            return result;
        }''')
        
        if apply_buttons:
            print("找到申请/投标按钮:")
            for btn in apply_buttons:
                print(f"  - {btn}")
        else:
            print("未找到明显的投标按钮，可能需要登录后显示")
        
        # 提取项目详情
        print("\n6️⃣ 提取项目详情...")
        content = page.evaluate('''() => {
            const result = [];
            document.querySelectorAll('*').forEach(el => {
                const text = (el.innerText || '').trim();
                if (text.length > 20 && text.length < 500) {
                    result.push(text);
                }
            });
            return result.slice(0, 30);
        }''')
        
        print("项目内容:")
        for i, text in enumerate(content[:20], 1):
            print(f"{i}. {text}")
    
    browser.close()
    
    print("\n✅ 探索完成")
    
except Exception as e:
    print(f"❌ 错误：{e}")
