#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

print("🔍 检查小红书登录方式...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=True, 
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    page.goto('https://www.xiaohongshu.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            buttons: [],
            inputs: []
        };
        
        document.querySelectorAll('button, input').forEach(el => {
            const text = (el.innerText || el.textContent || el.placeholder || '').trim();
            if (text && (text.includes('登录') || text.includes('注册') || text.includes('手机') || text.includes('验证码') || text.includes('密码'))) {
                if (el.tagName === 'BUTTON') data.buttons.push(text);
                if (el.tagName === 'INPUT') data.inputs.push({type: el.type, placeholder: text});
            }
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    print(f"\n🔘 登录按钮：{result['buttons']}")
    print(f"📝 输入框：{result['inputs']}")
    
    page.screenshot(path='/root/.openclaw/workspace/xiaohongshu_login_check.png', full_page=True)
    print("📸 已截图")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
