#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"

print("📱 小红书短信登录测试")
print("="*50)
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
    
    # 访问首页
    print("\n1️⃣ 访问小红书首页...")
    page.goto('https://www.xiaohongshu.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/xhs_home.png', full_page=True)
    print("2️⃣ 已截图：xhs_home.png")
    
    # 点击登录按钮
    print("3️⃣ 点击登录...")
    clicked = page.evaluate('''() => {
        const buttons = document.querySelectorAll('button, a, span, div');
        for (let btn of buttons) {
            const text = (btn.innerText || '').trim();
            if (text.includes('登录') || text.includes('登陆')) {
                btn.click();
                console.log('点击了登录按钮:', text);
                return true;
            }
        }
        return false;
    }''')
    print(f"登录按钮点击：{clicked}")
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/xhs_login_modal.png', full_page=True)
    print("4️⃣ 已截图：xhs_login_modal.png")
    
    # 分析登录弹窗
    result = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            inputs: [],
            buttons: [],
            hasSlider: false,
            hasCaptcha: false
        };
        
        document.querySelectorAll('input').forEach(el => {
            data.inputs.push({
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder
            });
        });
        
        document.querySelectorAll('button, span[role="button"]').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text) data.buttons.push(text);
        });
        
        // 检查滑块验证
        data.hasSlider = !!document.querySelector('.nc-container') || 
                        !!document.querySelector('#nc_1') ||
                        !!document.querySelector('.slider');
        
        // 检查图片验证码
        const allText = document.body.innerText.toLowerCase();
        data.hasCaptcha = allText.includes('验证码') && allText.includes('图片');
        
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
    print(f"\n🔍 滑块验证：{'是' if result['hasSlider'] else '否'}")
    print(f"🔍 图片验证码：{'是' if result['hasCaptcha'] else '否'}")
    
    # 输入手机号
    print(f"\n5️⃣ 输入手机号：{PHONE}...")
    phone_result = page.evaluate(f'''() => {{
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
    print(f"手机号输入：{phone_result}")
    time.sleep(2)
    
    # 找获取验证码按钮并点击
    print("6️⃣ 点击获取验证码...")
    sms_result = page.evaluate('''() => {
        const buttons = document.querySelectorAll('button, span, a, div');
        for (let btn of buttons) {
            const text = (btn.innerText || '').trim();
            if (text.includes('获取') || text.includes('发送') || text.includes('验证码') || text.includes('获取验证码')) {
                btn.click();
                console.log('点击了按钮:', text);
                return { success: true, text: text };
            }
        }
        return { success: false, text: null };
    }''')
    print(f"验证码按钮点击：{sms_result}")
    time.sleep(3)
    
    # 最终截图
    page.screenshot(path='/root/.openclaw/workspace/xhs_sms_sent.png', full_page=True)
    print("7️⃣ 已截图：xhs_sms_sent.png")
    
    # 检查是否有错误提示
    messages = page.evaluate('''() => {
        const msgs = [];
        document.querySelectorAll('.error, .message, .tip, .notice, .toast').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && text.length < 200) msgs.push(text);
        });
        return msgs;
    }''')
    
    if messages:
        print(f"\n⚠️  页面提示:")
        for msg in messages[:5]:
            print(f"  - {msg}")
    
    # 保存 Cookie
    cookies = context.cookies()
    with open('/root/.openclaw/workspace/xhs_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)
    print("\n💾 Cookie 已保存")
    
    print("\n" + "="*50)
    print("✅ 小红书登录流程完成")
    print("📱 请检查手机是否收到验证码")
    print("📸 查看截图：xhs_sms_sent.png")
    print("="*50)
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
