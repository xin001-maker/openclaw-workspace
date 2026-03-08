#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

PHONE = "13192195866"

print("📱 尝试淘宝登录（闲鱼共用账号）...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=True, 
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 访问淘宝登录页
    print("访问淘宝登录页...")
    page.goto('https://login.taobao.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/taobao_login.png', full_page=True)
    print("已截图：taobao_login.png")
    
    # 获取页面所有元素
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            inputs: [],
            buttons: [],
            links: []
        };
        
        document.querySelectorAll('input').forEach(el => {
            data.inputs.push({
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder,
                class: el.className
            });
        });
        
        document.querySelectorAll('button, a').forEach(el => {
            const text = (el.innerText || el.textContent || '').trim();
            if (text) {
                if (el.tagName === 'BUTTON') {
                    data.buttons.push(text);
                } else {
                    data.links.push({text, href: el.href});
                }
            }
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    print(f"\n📝 输入框 ({len(result['inputs'])}个):")
    for inp in result['inputs'][:10]:
        print(f"  - {inp}")
    print(f"\n🔘 按钮 ({len(result['buttons'])}个):")
    for btn in result['buttons'][:10]:
        print(f"  - {btn}")
    print(f"\n🔗 链接 ({len(result['links'])}个):")
    for link in result['links'][:10]:
        print(f"  - {link['text'][:30]}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
