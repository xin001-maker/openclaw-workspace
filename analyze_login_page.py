#!/usr/bin/env python3
# 详细分析登录页面结构

from playwright.sync_api import sync_playwright
import time
import json

print("🔍 详细分析闲鱼登录页面结构...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 访问发布页面
    page.goto('https://www.goofish.com/publish', timeout=30000, wait_until='domcontentloaded')
    time.sleep(5)
    
    # 获取完整 HTML
    html = page.content()
    
    # 保存 HTML 到文件
    with open('/root/.openclaw/workspace/login_page.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ 已保存页面 HTML: login_page.html")
    
    # 提取所有表单元素
    print("\n📋 所有表单元素：")
    elements = page.evaluate('''() => {
        const inputs = document.querySelectorAll('input, button, select, textarea');
        return Array.from(inputs).map(el => ({
            tag: el.tagName,
            type: el.type,
            name: el.name,
            id: el.id,
            placeholder: el.placeholder,
            text: el.innerText,
            class: el.className
        })).filter(el => el.placeholder || el.text || el.name || el.id);
    }''')
    
    for i, el in enumerate(elements[:20]):  # 最多显示 20 个
        print(f"\n{i+1}. {el['tag']}")
        if el['type']: print(f"   type: {el['type']}")
        if el['name']: print(f"   name: {el['name']}")
        if el['id']: print(f"   id: {el['id']}")
        if el['placeholder']: print(f"   placeholder: {el['placeholder']}")
        if el['text']: print(f"   text: {el['text'][:50]}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/login_page_full.png', full_page=True)
    print("\n📸 已截图：login_page_full.png")
    
    browser.close()
    print("\n✅ 分析完成")
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
