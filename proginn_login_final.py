#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"
PASSWORD = "J.o123456"

print("🔐 程序员客栈登录")
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
    
    # 访问首页
    print("1️⃣ 访问首页...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 点击登录
    print("2️⃣ 点击登录...")
    page.evaluate('''() => {
        const all = document.querySelectorAll('*');
        for (let el of all) {
            const text = (el.innerText || '').trim();
            if (text === '登录') {
                el.click();
                return true;
            }
        }
        return false;
    }''')
    time.sleep(3)
    
    # 输入账号密码
    print("3️⃣ 输入账号密码...")
    login_result = page.evaluate(f'''() => {{
        const phone = "{PHONE}";
        const password = "{PASSWORD}";
        
        const inputs = document.querySelectorAll('input');
        let phoneFilled = false;
        let passwordFilled = false;
        
        for (let input of inputs) {{
            const type = input.type;
            const placeholder = (input.placeholder || '').toLowerCase();
            const name = (input.name || '').toLowerCase();
            
            // 找手机号/账号输入框
            if (!phoneFilled && (type === 'text' || type === 'tel' || type === 'number')) {{
                if (placeholder.includes('手机') || placeholder.includes('账号') || 
                    placeholder.includes('phone') || name.includes('phone') || name.includes('account')) {{
                    input.value = phone;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    phoneFilled = true;
                    console.log('手机号输入框:', input);
                    continue;
                }}
            }}
            
            // 找密码输入框
            if (!passwordFilled && type === 'password') {{
                input.value = password;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                passwordFilled = true;
                console.log('密码输入框:', input);
                continue;
            }}
        }}
        
        // 找登录按钮
        const buttons = document.querySelectorAll('button, input[type="submit"], div[role="button"]');
        for (let btn of buttons) {{
            const text = (btn.innerText || '').trim();
            if (text.includes('登录') || text.includes('Login')) {{
                btn.click();
                console.log('点击登录按钮:', text);
                return {{ success: true, phoneFilled, passwordFilled, clicked: true }};
            }}
        }}
        
        return {{ success: false, phoneFilled, passwordFilled, clicked: false }};
    }}''')
    
    print(f"登录操作：{login_result}")
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_login_attempt.png', full_page=True)
    print("4️⃣ 已截图：proginn_login_attempt.png")
    
    # 检查登录状态
    status = page.evaluate('''() => {
        const url = window.location.href;
        const title = document.title;
        
        if (url.includes('/user/center') || url.includes('/dashboard') || url.includes('/release')) {
            return { logged_in: true, page: '成功页面', url: url };
        }
        if (url.includes('/login')) {
            return { logged_in: false, page: '仍在登录页', url: url };
        }
        return { logged_in: false, page: '其他页面', url: url };
    }''')
    
    print(f"\n🔐 登录状态：{status}")
    
    # 保存 Cookie
    cookies = context.cookies()
    with open('/root/.openclaw/workspace/proginn_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)
    print("\n💾 Cookie 已保存到：proginn_cookies.json")
    
    browser.close()
    
    print("\n" + "="*50)
    if status['logged_in']:
        print("✅ 登录成功！")
    else:
        print("⚠️  登录可能未成功")
        print(f"当前页面：{status['page']}")
    print("="*50)
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
