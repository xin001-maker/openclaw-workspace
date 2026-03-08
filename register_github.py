#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import random
import string
import json

# 生成随机用户名和密码
random_suffix = ''.join(random.choices(string.digits, k=6))
USERNAME = f"openclaw-cn-{random_suffix}"
EMAIL = f"openclaw.cn.{random_suffix}@protonmail.com"
PASSWORD = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=16))

print("🔧 GitHub 账号注册")
print("="*50)
print(f"用户名：{USERNAME}")
print(f"邮箱：{EMAIL}")
print(f"密码：{PASSWORD}")
print("="*50)

# 保存账号信息
account_info = {
    "platform": "GitHub",
    "username": USERNAME,
    "email": EMAIL,
    "password": PASSWORD,
    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
}

with open('/root/.openclaw/workspace/github_account.json', 'w') as f:
    json.dump(account_info, f, indent=2)

print("\n💾 账号信息已保存到：github_account.json")

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
    
    # 访问 GitHub 注册页
    print("\n1️⃣ 访问 GitHub 注册页...")
    page.goto('https://github.com/signup', timeout=30000, wait_until='domcontentloaded')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/github_signup.png', full_page=True)
    print("2️⃣ 已截图：github_signup.png")
    
    # 获取页面元素
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
                placeholder: el.placeholder,
                value: el.value
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
    print(f"\n📝 输入框 ({len(result['inputs'])}个):")
    for inp in result['inputs'][:10]:
        print(f"  - {inp}")
    print(f"\n🔘 按钮 ({len(result['buttons'])}个):")
    for btn in result['buttons'][:5]:
        print(f"  - {btn}")
    
    browser.close()
    
    print("\n⚠️  GitHub 注册可能需要邮箱验证，临时邮箱可能无法接收")
    print("💡 建议：使用真实邮箱注册更可靠")
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
