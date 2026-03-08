#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"
PASSWORD = "J.o123456"

print("🔐 程序员客栈登录 - 详细分析")

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
    print("\n1️⃣ 访问首页...")
    page.goto('https://www.proginn.com', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 获取所有链接
    links = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a').forEach(el => {
            const text = (el.innerText || '').trim();
            const href = el.href;
            if (text && (text.includes('登录') || text.includes('注册'))) {
                result.push({text, href});
            }
        });
        return result;
    }''')
    
    print(f"\n🔗 登录/注册链接:")
    for link in links[:10]:
        print(f"  - {link['text']}: {link['href'][:80]}")
    
    # 访问登录页
    print("\n2️⃣ 访问登录页...")
    page.goto('https://www.proginn.com/user/login', timeout=30000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_login_page.png', full_page=True)
    print("3️⃣ 已截图：proginn_login_page.png")
    
    # 详细分析页面元素
    page_info = page.evaluate('''() => {
        const data = {
            url: window.location.href,
            title: document.title,
            inputs: [],
            buttons: [],
            forms: []
        };
        
        document.querySelectorAll('input').forEach(el => {
            data.inputs.push({
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder,
                class: el.className
            });
        });
        
        document.querySelectorAll('button').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text) data.buttons.push(text);
        });
        
        document.querySelectorAll('form').forEach((el, i) => {
            data.forms.push({
                id: el.id,
                class: el.className,
                action: el.action
            });
        });
        
        return data;
    }''')
    
    print(f"\n📄 URL: {page_info['url']}")
    print(f"📄 Title: {page_info['title']}")
    
    print(f"\n📝 输入框 ({len(page_info['inputs'])}个):")
    for i, inp in enumerate(page_info['inputs'][:10]):
        print(f"  {i+1}. type={inp['type']}, name={inp['name']}, placeholder={inp['placeholder']}")
    
    print(f"\n🔘 按钮 ({len(page_info['buttons'])}个):")
    for i, btn in enumerate(page_info['buttons'][:10]):
        print(f"  {i+1}. {btn}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
