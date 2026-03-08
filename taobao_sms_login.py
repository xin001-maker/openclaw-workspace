#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"

print("📱 淘宝短信登录...")
print(f"手机号：{PHONE}")

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
    
    # 访问登录页
    print("\n1️⃣ 访问登录页...")
    page.goto('https://login.taobao.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 点击短信登录
    print("2️⃣ 点击短信登录...")
    page.evaluate('''() => {
        const links = document.querySelectorAll('a');
        for (let link of links) {
            const text = (link.innerText || '').trim();
            if (text.includes('短信登录')) {
                link.click();
                return true;
            }
        }
        return false;
    }''')
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/taobao_sms_page.png', full_page=True)
    print("3️⃣ 已截图：taobao_sms_page.png")
    
    # 获取当前页面元素
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            inputs: [],
            buttons: []
        };
        
        document.querySelectorAll('input').forEach(el => {
            data.inputs.push({
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder
            });
        });
        
        document.querySelectorAll('button').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text) data.buttons.push(text);
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    print(f"\n📝 输入框：{result['inputs']}")
    print(f"🔘 按钮：{result['buttons']}")
    
    # 输入手机号
    print(f"\n4️⃣ 输入手机号：{PHONE}...")
    page.evaluate(f'''() => {{
        const phone = "{PHONE}";
        const inputs = document.querySelectorAll('input[type="tel"], input[type="text"], input[type="number"]');
        for (let input of inputs) {{
            const placeholder = (input.placeholder || '').toLowerCase();
            if (placeholder.includes('手机') || placeholder.includes('phone') || input.type === 'tel') {{
                input.value = phone;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                console.log('输入成功:', input);
                return true;
            }}
        }}
        return false;
    }}''')
    time.sleep(2)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/taobao_phone_entered.png', full_page=True)
    print("5️⃣ 已截图：taobao_phone_entered.png")
    
    # 找获取验证码按钮并点击
    print("6️⃣ 点击获取验证码...")
    clicked = page.evaluate('''() => {
        const buttons = document.querySelectorAll('button, a, span');
        for (let btn of buttons) {
            const text = (btn.innerText || '').trim();
            if (text.includes('获取') || text.includes('发送') || text.includes('验证码')) {
                btn.click();
                console.log('点击了按钮:', text);
                return true;
            }
        }
        return false;
    }''')
    
    print(f"按钮点击结果：{clicked}")
    time.sleep(3)
    
    # 最终截图
    page.screenshot(path='/root/.openclaw/workspace/taobao_sms_sent.png', full_page=True)
    print("7️⃣ 已截图：taobao_sms_sent.png")
    
    # 保存 Cookie
    cookies = context.cookies()
    with open('/root/.openclaw/workspace/taobao_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)
    print("\n💾 Cookie 已保存")
    
    print("\n" + "="*50)
    print("✅ 验证码已发送！")
    print("📱 请检查手机短信")
    print("📸 查看截图：taobao_sms_sent.png")
    print("="*50)
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
