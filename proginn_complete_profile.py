#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📝 完善程序员客栈个人资料")
print("="*50)

# 加载 Cookie
with open('/root/.openclaw/workspace/proginn_cookies.json', 'r') as f:
    cookies = json.load(f)

# 个人资料内容
PROFILE_DATA = {
    'skills': ['Python', '自动化脚本', '数据处理', '网页爬虫', 'AI 应用', 'Excel 自动化'],
    'intro': '''Python 开发工程师，专注自动化开发

【核心技能】
• Python 开发（5 年经验）
• 自动化脚本开发
• 数据处理与分析（pandas）
• 网页爬虫（Playwright/Selenium）
• AI 应用集成（LLM API）

【代表项目】
• Python 效率工具箱：https://github.com/xin001-maker/python-efficiency-tools
• 文件批量处理系统
• Excel 自动化报表生成
• 图片批量压缩工具

【服务承诺】
• 快速响应（2 小时内）
• 按时交付
• 提供完整源代码和文档
• 7 天免费维护''',
    'expectations': '500-2000 元/项目'
}

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 访问个人中心
    print("1️⃣ 访问个人中心...")
    page.goto('https://www.proginn.com/user/center', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_center.png', full_page=True)
    print("2️⃣ 已截图：proginn_center.png")
    
    # 获取页面信息
    page_info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            hasProfile: !!document.querySelector('.profile') || !!document.querySelector('.user-info'),
            inputCount: document.querySelectorAll('input, textarea').length
        };
    }''')
    
    print(f"\n📄 URL: {page_info['url']}")
    print(f"📄 Title: {page_info['title']}")
    print(f"📝 输入框数量：{page_info['inputCount']}")
    
    # 尝试填写个人简介
    print("\n3️⃣ 尝试填写个人简介...")
    fill_result = page.evaluate(f'''() => {{
        const intro = `{PROFILE_DATA['intro']}`;
        
        // 找简介输入框
        const textareas = document.querySelectorAll('textarea');
        let filled = false;
        for (let ta of textareas) {{
            const placeholder = (ta.placeholder || '').toLowerCase();
            if (placeholder.includes('简介') || placeholder.includes('介绍') || placeholder.includes('self')) {{
                ta.value = intro;
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                filled = true;
                console.log('已填写简介');
                break;
            }}
        }}
        
        // 找技能标签输入
        const inputs = document.querySelectorAll('input[type="text"]');
        let skillsFound = false;
        for (let inp of inputs) {{
            const placeholder = (inp.placeholder || '').toLowerCase();
            if (placeholder.includes('技能') || placeholder.includes('tag')) {{
                skillsFound = true;
                console.log('找到技能输入框');
                break;
            }}
        }}
        
        return {{ filled, skillsFound, textareaCount: textareas.length }};
    }}''')
    
    print(f"填写结果：{fill_result}")
    time.sleep(3)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_profile_filled.png', full_page=True)
    print("4️⃣ 已截图：proginn_profile_filled.png")
    
    browser.close()
    
    print("\n" + "="*50)
    print("✅ 资料填写尝试完成")
    print("请检查截图确认填写效果")
    print("="*50)
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
