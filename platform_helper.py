#!/usr/bin/env python3
# 闲鱼/小红书登录和发布辅助脚本

from playwright.sync_api import sync_playwright
import time
import json

class PlatformHelper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
    
    def launch(self, platform):
        """启动浏览器"""
        print(f"\n🚀 启动 {platform}...")
        
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=False,  # 显示浏览器，方便人工操作
            args=['--no-sandbox']
        )
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
        print("✅ 浏览器已启动")
    
    def login_xianyu(self):
        """登录闲鱼"""
        print("\n📱 闲鱼登录")
        print("⚠️  闲鱼网页版功能有限，建议用 APP 发布")
        print("📍 正在访问闲鱼...")
        
        self.page.goto("https://www.xianyu.com", timeout=30000)
        time.sleep(5)
        
        print("\n💡 操作指引：")
        print("1. 如果未登录，点击右上角登录")
        print("2. 用淘宝/支付宝扫码登录")
        print("3. 登录后可以查看已发布的商品")
        print("\n⏳ 等待 60 秒供你操作...")
        time.sleep(60)
    
    def publish_xianyu(self, title, price, description, image_path):
        """发布闲鱼商品"""
        print(f"\n📦 发布商品：{title}")
        
        # 导航到发布页面
        self.page.goto("https://www.xianyu.com/release", timeout=30000)
        time.sleep(3)
        
        print("\n💡 操作指引：")
        print(f"1. 上传图片：{image_path}")
        print(f"2. 标题：{title}")
        print(f"3. 价格：{price}")
        print(f"4. 描述：{description[:50]}...")
        print("\n⏳ 等待 120 秒供你操作...")
        time.sleep(120)
    
    def login_xiaohongshu(self):
        """登录小红书"""
        print("\n📕 小红书登录")
        print("📍 正在访问小红书...")
        
        self.page.goto("https://www.xiaohongshu.com", timeout=30000)
        time.sleep(5)
        
        print("\n💡 操作指引：")
        print("1. 如果未登录，点击右上角登录")
        print("2. 可以用手机号/微信扫码登录")
        print("3. 登录后可以发布笔记")
        print("\n⏳ 等待 60 秒供你操作...")
        time.sleep(60)
    
    def publish_xiaohongshu(self, title, content):
        """发布小红书笔记"""
        print(f"\n📝 发布笔记：{title}")
        
        # 导航到发布页面
        self.page.goto("https://www.xiaohongshu.com/publish", timeout=30000)
        time.sleep(3)
        
        print("\n💡 操作指引：")
        print(f"1. 上传图片/视频")
        print(f"2. 标题：{title}")
        print(f"3. 内容：{content[:50]}...")
        print("\n⏳ 等待 120 秒供你操作...")
        time.sleep(120)
    
    def save_cookies(self, filename):
        """保存 Cookie"""
        cookies = self.context.cookies()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"✅ Cookie 已保存到：{filename}")
    
    def load_cookies(self, filename):
        """加载 Cookie"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            self.context.add_cookies(cookies)
            print(f"✅ Cookie 已加载：{filename}")
            return True
        except:
            print(f"❌ Cookie 加载失败：{filename}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            print("👋 浏览器已关闭")

# 使用示例
if __name__ == "__main__":
    helper = PlatformHelper()
    
    try:
        # 选择平台
        print("\n=== 平台登录助手 ===")
        print("1. 闲鱼")
        print("2. 小红书")
        print("3. 退出")
        
        choice = input("\n请选择 (1/2/3): ").strip()
        
        if choice == "1":
            helper.launch("闲鱼")
            helper.login_xianyu()
            helper.save_cookies("/root/.openclaw/workspace/xianyu_cookies.json")
        elif choice == "2":
            helper.launch("小红书")
            helper.login_xiaohongshu()
            helper.save_cookies("/root/.openclaw/workspace/xiaohongshu_cookies.json")
        elif choice == "3":
            print("👋 退出")
        else:
            print("❌ 无效选择")
    
    finally:
        helper.close()
