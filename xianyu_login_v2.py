#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

PHONE = "13192195866"

print("🔍 详细分析闲鱼登录页面...")

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=False,  # 有头模式看看
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = context.new_page()
    
    # 访问首页
    print("访问首页...")
    page.goto('https://www.goofish.com', timeout=30000, wait_until='networkidle')
    time.sleep(5)
    
    # 保存 HTML
    with open('/root/.openclaw/workspace/goofish_home_debug.html', 'w', encoding='utf-8') as f:
        f.write(page.content())
    print("已保存 HTML")
    
    # 获取所有可点击元素
    elements = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a, button, span, div').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text && text.length < 50 && (text.includes('登录') || text.includes('登'))) {
                result.push({
                    tag: el.tagName,
                    text: text,
                    class: el.className,
                    id: el.id,
                    clickable: el.onclick !== null || el.getAttribute('role') === 'button'
                });
            }
        });
        return result;
    }''')
    
    print(f"\n找到登录相关元素：{len(elements)}")
    for el in elements[:20]:
        print(f"  - {el}")
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/goofish_home_debug.png', full_page=True)
    print("\n已截图")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
