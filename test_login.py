#!/usr/bin/env python3
# 测试登录闲鱼和小红书

from playwright.sync_api import sync_playwright
import time

def test_xianyu():
    """测试闲鱼网页版"""
    print("\n=== 测试闲鱼网页版 ===")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print("访问闲鱼网页版...")
            page.goto("https://www.xianyu.com", timeout=30000)
            time.sleep(3)
            
            # 检查是否已登录
            page_content = page.content()
            if "登录" in page_content or "login" in page_content.lower():
                print("⚠️  检测到未登录状态")
            else:
                print("✅  可能已登录")
            
            print("📱 闲鱼网页版功能有限，主要功能在 APP")
            print("💡 建议：使用 APP 发布，或保存 Cookie 后用自动化脚本")
            
            # 截图
            page.screenshot(path='/root/.openclaw/workspace/xianyu_test.png')
            print("📸 已截图：xianyu_test.png")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
        
        print("\n⏳ 请在浏览器中尝试登录（如果需要）")
        input("完成后按回车继续...")
        browser.close()

def test_xiaohongshu():
    """测试小红书网页版"""
    print("\n=== 测试小红书网页版 ===")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print("访问小红书网页版...")
            page.goto("https://www.xiaohongshu.com", timeout=30000)
            time.sleep(3)
            
            # 检查是否已登录
            page_content = page.content()
            if "登录" in page_content or "login" in page_content.lower():
                print("⚠️  检测到未登录状态")
            else:
                print("✅  可能已登录")
            
            print("📱 小红书网页版可以发布笔记，但功能不如 APP 全")
            
            # 截图
            page.screenshot(path='/root/.openclaw/workspace/xiaohongshu_test.png')
            print("📸 已截图：xiaohongshu_test.png")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
        
        print("\n⏳ 请在浏览器中尝试登录（如果需要）")
        input("完成后按回车继续...")
        browser.close()

if __name__ == "__main__":
    print("🚀 开始测试平台登录...")
    print("\n⚠️  注意：")
    print("1. 闲鱼网页版功能有限，主要用 APP")
    print("2. 小红书网页版可以发布笔记")
    print("3. 登录可能需要短信验证码")
    print("\n按回车开始测试闲鱼...")
    input()
    
    test_xianyu()
    
    print("\n按回车开始测试小红书...")
    input()
    
    test_xiaohongshu()
    
    print("\n✅ 测试完成！")
