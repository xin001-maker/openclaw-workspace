#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

print("🔍 检查闲鱼登录页面可用的登录方式...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    page.goto('https://www.goofish.com/login', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            allText: [],
            inputs: [],
            buttons: [],
            links: []
        };
        
        document.querySelectorAll('input, button, a, span, div, p, label').forEach(el => {
            const text = (el.innerText || el.textContent || '').trim();
            if (text.length > 0 && text.length < 100) {
                data.allText.push(text);
            }
            if (el.tagName === 'INPUT') {
                data.inputs.push({type: el.type, placeholder: el.placeholder, name: el.name, id: el.id});
            } else if (el.tagName === 'BUTTON') {
                data.buttons.push(text);
            } else if (el.tagName === 'A') {
                data.links.push({text: text, href: el.href});
            }
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    
    print("\n🔘 所有按钮:")
    for btn in result['buttons'][:20]:
        print(f"  - {btn}")
    
    print("\n📝 输入框:")
    for inp in result['inputs'][:20]:
        print(f"  - {inp}")
    
    print("\n🔗 链接:")
    for link in result['links'][:20]:
        if link['text'] or 'login' in link['href'].lower():
            print(f"  - {link['text']}: {link['href'][:100]}")
    
    print("\n📋 页面文本 (前 50 条):")
    for text in result['allText'][:50]:
        print(f"  - {text}")
    
    page.screenshot(path='/root/.openclaw/workspace/login_page_methods.png', full_page=True)
    print("\n📸 已截图：login_page_methods.png")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
