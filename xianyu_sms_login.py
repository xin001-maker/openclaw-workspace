#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"

print(f"📱 开始闲鱼短信登录流程...")
print(f"手机号：{PHONE}")

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
    
    # 访问登录页面
    print("\n📄 访问登录页面...")
    page.goto('https://www.goofish.com/login', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/login_before_sms.png', full_page=True)
    print("📸 已截图：login_before_sms.png")
    
    # 尝试找到手机号输入框并输入
    print(f"\n🔢 输入手机号：{PHONE}...")
    
    result = page.evaluate(f'''() => {{
        const phone = "{PHONE}";
        let found = false;
        
        // 找手机号输入框
        const inputs = document.querySelectorAll('input[type="tel"], input[type="text"], input[type="number"]');
        for (let input of inputs) {{
            const placeholder = (input.placeholder || '').toLowerCase();
            const name = (input.name || '').toLowerCase();
            const id = (input.id || '').toLowerCase();
            
            if (placeholder.includes('手机') || placeholder.includes('phone') || 
                name.includes('phone') || name.includes('mobile') ||
                id.includes('phone') || id.includes('mobile')) {{
                input.value = phone;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                console.log('找到手机号输入框:', input);
                found = true;
                break;
            }}
        }}
        
        // 如果没找到，尝试所有输入框
        if (!found) {{
            for (let input of inputs) {{
                if (input.type === 'tel' || input.type === 'number') {{
                    input.value = phone;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    console.log('尝试输入到:', input);
                    found = true;
                    break;
                }}
            }}
        }}
        
        return {{ found, inputCount: inputs.length }};
    }}''')
    
    print(f"结果：{result}")
    
    # 找获取验证码按钮
    print("\n🔍 查找获取验证码按钮...")
    
    button_result = page.evaluate('''() => {
        const buttons = document.querySelectorAll('button, a, span, div');
        let found = null;
        
        for (let btn of buttons) {
            const text = (btn.innerText || btn.textContent || '').trim();
            if (text.includes('获取验证码') || text.includes('发送验证码') || 
                text.includes('获取') || text.includes('发送')) {
                found = { text, tagName: btn.tagName, className: btn.className };
                btn.style.border = '3px solid red';
                console.log('找到按钮:', btn);
                break;
            }
        }
        
        return found;
    }''')
    
    print(f"按钮：{button_result}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/login_after_input.png', full_page=True)
    print("📸 已截图：login_after_input.png")
    
    print("\n✅ 登录页面准备完成")
    print("📱 请检查手机是否收到验证码")
    print("📸 截图已保存，请查看页面状态")
    
    # 保存上下文用于后续
    print("\n⏳ 等待验证码...")
    print("收到验证码后告诉我，我继续输入")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
