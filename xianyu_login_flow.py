#!/usr/bin/env python3
# 闲鱼登录流程 - 直接访问发布页（会跳转登录）

from playwright.sync_api import sync_playwright
import time

print("🚀 访问闲鱼发布页面（会自动跳转登录）...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 直接访问发布页面（会跳转登录）
    print("\n📱 访问：https://www.goofish.com/publish")
    page.goto('https://www.goofish.com/publish', timeout=30000, wait_until='domcontentloaded')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/goofish_publish_login.png', full_page=True)
    print("📸 已截图：goofish_publish_login.png")
    
    # 获取页面内容分析
    content = page.content()
    
    print("\n🔍 分析登录表单...")
    
    # 检查是否有手机号输入
    if 'phone' in content.lower() or 'mobile' in content.lower() or '手机' in content:
        print("✅ 检测到手机号输入框")
    else:
        print("❌ 未找到手机号输入框")
    
    # 检查是否有验证码
    if 'code' in content.lower() or 'verify' in content.lower() or '验证码' in content:
        print("✅ 检测到验证码输入框")
    else:
        print("❌ 未找到验证码输入框")
    
    # 检查是否有获取验证码按钮
    if '获取' in content or '发送' in content or 'Get' in content:
        print("✅ 检测到获取验证码按钮")
    else:
        print("❌ 未找到获取验证码按钮")
    
    # 提取所有输入框
    print("\n📋 页面输入元素：")
    inputs = page.query_selector_all('input')
    for i, inp in enumerate(inputs[:10]):  # 最多显示 10 个
        try:
            placeholder = inp.get_attribute('placeholder')
            input_type = inp.get_attribute('type')
            input_name = inp.get_attribute('name')
            print(f"  {i+1}. type={input_type}, name={input_name}, placeholder={placeholder}")
        except:
            pass
    
    # 提取所有按钮
    print("\n📋 页面按钮：")
    buttons = page.query_selector_all('button')
    for i, btn in enumerate(buttons[:10]):  # 最多显示 10 个
        try:
            text = btn.inner_text()
            btn_type = btn.get_attribute('type')
            print(f"  {i+1}. {btn_type} - {text[:50]}")
        except:
            pass
    
    browser.close()
    print("\n✅ 分析完成")
    print("\n📸 截图：/root/.openclaw/workspace/goofish_publish_login.png")
    
except Exception as e:
    print(f"❌ 错误：{e}")
