#!/usr/bin/env python3
"""
程序员客栈自动投标脚本 v2
使用新 cookies 尝试登录和投标
"""
from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

print("🚀 程序员客栈自动投标 v2")
print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 尝试使用新 cookies
    print("1️⃣ 加载新 cookies...")
    try:
        with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"✅ 加载了 {len(cookies)} 个 cookies")
    except Exception as e:
        print(f"⚠️ 读取 cookies 失败：{e}")
        cookies = []
    
    # 访问首页验证登录状态
    print("2️⃣ 验证登录状态...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_login_check_v2.png', full_page=True)
    print("📸 截图已保存")
    
    # 检查是否登录成功
    is_logged_in = page.evaluate('''() => {
        const text = document.body.innerText;
        // 检查登录相关关键词
        if (text.includes('退出') || text.includes('个人中心') || text.includes('我的项目')) {
            return true;
        }
        // 检查是否有登录按钮
        if (text.includes('登录') || text.includes('注册')) {
            return false;
        }
        return null; // 不确定
    }''')
    
    if is_logged_in == True:
        print("✅ 登录状态有效")
        
        # 访问项目列表
        print("3️⃣ 访问项目列表...")
        page.goto('https://www.proginn.com/remote', timeout=60000, wait_until='networkidle')
        time.sleep(5)
        
        # 查找项目
        projects = page.evaluate('''() => {
            const result = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.href;
                const text = (a.innerText || '').trim();
                if (href && href.includes('/p/') && text.length > 10) {
                    result.push({href, text: text.substring(0, 100)});
                }
            });
            return result.slice(0, 10);
        }''')
        
        print(f"找到 {len(projects)} 个项目:")
        for i, proj in enumerate(projects[:5], 1):
            print(f"  {i}. {proj['text'][:60]}")
        
        # 保存项目信息
        if projects:
            with open('/root/.openclaw/workspace/proginn_projects_v2.json', 'w', encoding='utf-8') as f:
                json.dump(projects, f, ensure_ascii=False, indent=2)
            print("✅ 项目列表已保存")
        
    elif is_logged_in == False:
        print("❌ 登录已过期，需要重新登录")
        
        # 尝试访问登录页
        print("4️⃣ 访问登录页...")
        page.goto('https://www.proginn.com/user/login', timeout=60000, wait_until='networkidle')
        time.sleep(3)
        
        # 截图登录页
        page.screenshot(path='/root/.openclaw/workspace/proginn_login_page_v2.png')
        print("📸 登录页截图已保存")
        
    else:
        print("⚠️ 无法确定登录状态")
    
    browser.close()
    
    print("\n✅ 检查完成")
    print(f"⏰ 结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
