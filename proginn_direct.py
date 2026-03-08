#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

PHONE = "13192195866"
PASSWORD = "J.o123456"

print("🔐 程序员客栈 - 尝试直接登录")

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
    
    # 访问首页，等待加载
    print("\n1️⃣ 访问首页，等待加载...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_home.png', full_page=True)
    print("2️⃣ 已截图：proginn_home.png")
    
    # 找登录按钮并点击
    print("3️⃣ 查找登录按钮...")
    clicked = page.evaluate('''() => {
        const all = document.querySelectorAll('*');
        for (let el of all) {
            const text = (el.innerText || '').trim();
            if (text === '登录' || text.includes('请登录')) {
                el.click();
                return { clicked: true, text: text, tag: el.tagName };
            }
        }
        return { clicked: false };
    }''')
    print(f"点击结果：{clicked}")
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_after_click.png', full_page=True)
    print("4️⃣ 已截图：proginn_after_click.png")
    
    # 等待并检查页面
    time.sleep(5)
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            inputCount: document.querySelectorAll('input').length,
            buttonCount: document.querySelectorAll('button').length,
            bodyLength: document.body.innerText.length
        };
    }''')
    
    print(f"\n📄 URL: {info['url']}")
    print(f"📄 Title: {info['title']}")
    print(f"📝 输入框：{info['inputCount']}个")
    print(f"🔘 按钮：{info['buttonCount']}个")
    print(f"📋 页面文本长度：{info['bodyLength']}")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
