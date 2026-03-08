#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

PHONE = "13192195866"

print("🔍 检查短信发送状态...")

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
    
    # 访问短信登录页
    page.goto('https://login.taobao.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(2)
    
    # 切换到短信登录
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
    time.sleep(2)
    
    # 检查是否有滑块验证或其他验证
    has_slider = page.evaluate('''() => {
        return !!document.querySelector('.nc-container') || 
               !!document.querySelector('#nc_1_n1z') ||
               !!document.querySelector('.btn_slide');
    }''')
    
    has_captcha = page.evaluate('''() => {
        const inputs = document.querySelectorAll('input');
        for (let inp of inputs) {
            const placeholder = (inp.placeholder || '').toLowerCase();
            if (placeholder.includes('验证码') && placeholder.includes('图片')) {
                return true;
            }
        }
        return false;
    }''')
    
    print(f"\n🔍 检测结果:")
    print(f"  滑块验证：{'是' if has_slider else '否'}")
    print(f"  图片验证码：{'是' if has_captcha else '否'}")
    
    # 获取所有提示消息
    messages = page.evaluate('''() => {
        const msgs = [];
        document.querySelectorAll('.error, .message, .tip, .notice, .hint').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && text.length < 200) msgs.push(text);
        });
        return msgs;
    }''')
    
    if messages:
        print(f"\n⚠️  页面提示:")
        for msg in messages[:5]:
            print(f"  - {msg}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/taobao_check_status.png', full_page=True)
    print("\n📸 已截图：taobao_check_status.png")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
