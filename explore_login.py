#!/usr/bin/env python3
# 闲鱼登录流程探索

from playwright.sync_api import sync_playwright
import time

print("🚀 闲鱼登录流程探索（headless 模式）...")
print("⏰ 开始时间:", time.strftime("%H:%M:%S"))

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 访问闲鱼首页
    print("\n📱 访问闲鱼首页...")
    page.goto('https://www.goofish.com/', timeout=30000)
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/goofish_home.png', full_page=True)
    print("📸 已截图首页：goofish_home.png")
    
    # 获取页面内容
    content = page.content()
    
    # 检查登录相关元素
    print("\n🔍 分析页面内容...")
    
    login_keywords = ['登录', 'login', '手机号', '验证码', '注册']
    found = []
    for kw in login_keywords:
        if kw in content.lower() or kw in content:
            found.append(kw)
    
    if found:
        print(f"✅ 检测到关键词：{found}")
    else:
        print("⚠️  未找到明显登录入口")
    
    # 尝试访问登录页面
    print("\n📱 尝试访问登录页面...")
    page.goto('https://login.goofish.com/', timeout=30000)
    time.sleep(5)
    page.screenshot(path='/root/.openclaw/workspace/goofish_login.png', full_page=True)
    print("📸 已截图登录页：goofish_login.png")
    
    # 检查是否有手机号输入框
    content = page.content()
    if 'phone' in content.lower() or '手机' in content:
        print("✅ 检测到手机号输入相关元素")
    if 'code' in content.lower() or '验证码' in content:
        print("✅ 检测到验证码输入相关元素")
    
    print("\n📋 页面元素分析完成")
    print("📸 截图位置：/root/.openclaw/workspace/")
    print("   - goofish_home.png (首页)")
    print("   - goofish_login.png (登录页)")
    
    browser.close()
    print("\n✅ 流程探索完成")
    
except Exception as e:
    print(f"❌ 错误：{e}")
