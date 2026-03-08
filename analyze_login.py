#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time, json

print("🔍 详细分析闲鱼登录页面...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    page.goto('https://www.goofish.com/publish', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 获取所有登录相关元素
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            loginMethods: [],
            inputs: [],
            buttons: [],
            links: []
        };
        
        // 找登录相关元素
        document.querySelectorAll('input, button, a').forEach(el => {
            const text = el.innerText || el.textContent || '';
            const placeholder = el.placeholder || '';
            const type = el.type || el.tagName.toLowerCase();
            const combined = (text + ' ' + placeholder).toLowerCase();
            
            if (combined.includes('登录') || combined.includes('login') || 
                combined.includes('手机') || combined.includes('phone') ||
                combined.includes('验证码') || combined.includes('code') ||
                combined.includes('密码') || combined.includes('password') ||
                combined.includes('淘宝') || combined.includes('支付宝') ||
                combined.includes('扫码') || combined.includes('qr')) {
                
                if (el.tagName === 'INPUT') {
                    data.inputs.push({type: el.type, placeholder: el.placeholder, name: el.name});
                } else if (el.tagName === 'BUTTON') {
                    data.buttons.push(text.trim());
                } else if (el.tagName === 'A') {
                    data.links.push(text.trim() || el.href);
                }
            }
        });
        
        return data;
    }''')
    
    print("\n📄 页面信息:")
    print(f"  URL: {result['url']}")
    print(f"  Title: {result['title']}")
    
    print("\n🔑 登录方式:")
    for method in result['loginMethods']:
        print(f"  - {method}")
    
    print("\n📝 输入框:")
    for inp in result['inputs']:
        print(f"  - {inp}")
    
    print("\n🔘 按钮:")
    for btn in result['buttons']:
        print(f"  - {btn}")
    
    print("\n🔗 链接:")
    for link in result['links']:
        print(f"  - {link}")
    
    # 保存页面 HTML 用于分析
    with open('/root/.openclaw/workspace/login_page_full.html', 'w', encoding='utf-8') as f:
        f.write(page.content())
    print("\n💾 已保存完整 HTML: login_page_full.html")
    
    page.screenshot(path='/root/.openclaw/workspace/login_analysis.png', full_page=True)
    print("📸 已截图：login_analysis.png")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
