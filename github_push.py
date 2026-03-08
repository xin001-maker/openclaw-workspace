#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("🚀 推送代码到 GitHub")
print("="*50)
print("用户名：xin001-maker")
print("仓库名：python-efficiency-tools")
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
    
    # 访问 GitHub
    print("\n1️⃣ 访问 GitHub...")
    page.goto('https://github.com/login', timeout=30000, wait_until='domcontentloaded')
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/github_login_page.png', full_page=True)
    print("2️⃣ 已截图：github_login_page.png")
    
    # 检查是否已登录
    is_logged_in = page.evaluate('''() => {
        return !!document.querySelector('[data-test-selector="orgs-nav"]') || 
               window.location.href.includes('/dashboard');
    }''')
    
    if is_logged_in:
        print("✅ 已登录 GitHub")
    else:
        print("⚠️  需要登录 GitHub")
        print("📝 请在浏览器中登录：https://github.com/login")
        print("登录后告诉我，我继续推送")
    
    # 获取页面信息
    result = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            loggedIn: !!document.querySelector('[data-test-selector="orgs-nav"]')
        };
    }''')
    
    print(f"\n📄 URL: {result['url']}")
    print(f"📄 Title: {result['title']}")
    print(f"🔐 登录状态：{'已登录' if result['loggedIn'] else '未登录'}")
    
    browser.close()
    
    print("\n" + "="*50)
    if result['loggedIn']:
        print("✅ GitHub 已登录，准备创建仓库...")
    else:
        print("⏳ 等待登录 GitHub...")
        print("请访问 https://github.com/login 登录")
    print("="*50)
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
