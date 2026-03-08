#!/usr/bin/env python3
# 测试 Playwright 是否能运行

from playwright.sync_api import sync_playwright

def test_browser():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            page.goto("https://www.example.com")
            title = page.title()
            print(f"✅ 浏览器测试成功！")
            print(f"页面标题：{title}")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

if __name__ == "__main__":
    test_browser()
