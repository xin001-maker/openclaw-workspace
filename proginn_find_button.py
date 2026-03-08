#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

PHONE = "13192195866"
PASSWORD = "J.o123456"

print("🔍 查找登录按钮...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 点击登录
    page.evaluate('''() => {
        document.querySelectorAll('*').forEach(el => {
            if ((el.innerText || '').trim() === '登录') el.click();
        });
    }''')
    time.sleep(3)
    
    # 找所有可点击元素
    buttons = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('button, a, div, span, input').forEach(el => {
            const text = (el.innerText || el.textContent || '').trim();
            const role = el.getAttribute('role');
            const type = el.type || el.tagName;
            const onclick = el.onclick ? 'has_onclick' : 'no_onclick';
            
            if (text && text.length < 50) {
                result.push({ tag: el.tagName, text: text.substring(0, 30), role, type, onclick });
            }
        });
        return result.filter(x => x.text.includes('登录') || x.text.includes('提交') || x.text.includes('确定') || x.role === 'button');
    }''')
    
    print(f"\n🔘 可能的登录按钮 ({len(buttons)}个):")
    for btn in buttons[:20]:
        print(f"  - <{btn['tag']}> {btn['text']} (role={btn['role']}, onclick={btn['onclick']})")
    
    # 尝试点击所有包含"登录"的元素
    print("\n🔨 尝试点击所有登录按钮...")
    clicked = page.evaluate(f'''() => {{
        const phone = "{PHONE}";
        const password = "{PASSWORD}";
        
        // 先填账号密码
        document.querySelectorAll('input').forEach(input => {{
            const placeholder = (input.placeholder || '').toLowerCase();
            if (input.type === 'text' || input.type === 'tel') {{
                if (placeholder.includes('手机') || placeholder.includes('账号')) {{
                    input.value = phone;
                }}
            }}
            if (input.type === 'password') {{
                input.value = password;
            }}
        }});
        
        // 点击所有登录相关元素
        let count = 0;
        document.querySelectorAll('*').forEach(el => {{
            const text = (el.innerText || '').trim();
            if (text.includes('登录')) {{
                el.click();
                count++;
                console.log('点击了:', text, el.tagName);
            }}
        }});
        return count;
    }}''')
    
    print(f"点击了 {clicked} 个元素")
    time.sleep(5)
    
    # 检查登录状态
    status = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            loggedIn: !window.location.href.includes('/login') && document.title.includes('程序员客栈')
        };
    }''')
    
    print(f"\n🔐 状态：{status}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
