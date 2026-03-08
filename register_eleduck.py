#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🔍 电鸭社区注册页面分析")
print("="*50)

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
    
    # 访问电鸭社区
    print("\n1️⃣ 访问电鸭社区...")
    page.goto('https://eleduck.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/eleduck_home.png', full_page=True)
    print("2️⃣ 已截图：eleduck_home.png")
    
    # 找注册/登录入口
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            authLinks: []
        };
        
        document.querySelectorAll('a').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && (text.includes('登录') || text.includes('注册') || text.includes('signin') || text.includes('signup'))) {
                data.authLinks.push({text, href: el.href});
            }
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    print(f"\n🔐 登录/注册链接:")
    for link in result['authLinks'][:10]:
        print(f"  - {link['text']}: {link['href'][:80]}")
    
    # 尝试访问注册页
    signup_url = None
    for link in result['authLinks']:
        if '注册' in link['text'] or 'signup' in link['text'].lower():
            signup_url = link['href']
            break
    
    if signup_url:
        print(f"\n3️⃣ 访问注册页：{signup_url}")
        page.goto(signup_url, timeout=30000, wait_until='domcontentloaded')
        time.sleep(3)
        
        page.screenshot(path='/root/.openclaw/workspace/eleduck_signup.png', full_page=True)
        print("4️⃣ 已截图：eleduck_signup.png")
        
        # 分析注册表单
        form_info = page.evaluate('''() => {
            const data = {
                inputs: [],
                buttons: [],
                requiresPhone: false
            };
            
            document.querySelectorAll('input').forEach(el => {
                const info = {
                    type: el.type,
                    name: el.name,
                    placeholder: el.placeholder
                };
                data.inputs.push(info);
                if (el.placeholder && el.placeholder.includes('手机')) {
                    data.requiresPhone = true;
                }
            });
            
            document.querySelectorAll('button').forEach(el => {
                const text = (el.innerText || '').trim();
                if (text) data.buttons.push(text);
            });
            
            return data;
        }''')
        
        print(f"\n📝 输入框 ({len(form_info['inputs'])}个):")
        for inp in form_info['inputs'][:10]:
            print(f"  - {inp}")
        print(f"\n🔘 按钮 ({len(form_info['buttons'])}个):")
        for btn in form_info['buttons'][:5]:
            print(f"  - {btn}")
        print(f"\n📱 需要手机验证：{'是' if form_info['requiresPhone'] else '否'}")
    
    browser.close()
    
    print("\n" + "="*50)
    print("✅ 电鸭社区分析完成")
    print("="*50)
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
