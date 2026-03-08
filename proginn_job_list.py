#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import json

print("📋 访问岗位列表页面")

with open('/root/.openclaw/workspace/proginn_cookies_new.json', 'r') as f:
    cookies = json.load(f)

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    context.add_cookies(cookies)
    page = context.new_page()
    
    # 先访问云端工作页面，然后点击"查看全部"
    print("1️⃣ 访问云端工作页面...")
    page.goto('https://www.proginn.com/cloud', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 查找并点击"查看全部"
    print("2️⃣ 查找'查看全部'链接...")
    view_all_url = page.evaluate('''() => {
        let url = null;
        document.querySelectorAll('a').forEach(a => {
            const text = (a.innerText || '').trim();
            if (text === '查看全部' && a.href) {
                url = a.href;
            }
        });
        return url;
    }''')
    
    if view_all_url:
        print(f"找到链接：{view_all_url}")
        page.goto(view_all_url, timeout=60000, wait_until='networkidle')
        time.sleep(5)
    else:
        # 尝试常见 URL
        print("未找到'查看全部'，尝试常见 URL...")
        page.goto('https://www.proginn.com/cloud/positions', timeout=60000, wait_until='networkidle')
        time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_job_list.png', full_page=True)
    print("3️⃣ 截图已保存")
    
    # 获取页面信息
    info = page.evaluate('''() => {
        return {
            url: window.location.href,
            title: document.title,
            bodyLength: document.body.innerText.length,
        };
    }''')
    
    print(f"\n📄 URL: {info['url'][:100]}")
    print(f"📄 Title: {info['title'][:60]}")
    print(f"📄 内容长度：{info['bodyLength']}")
    
    # 提取岗位/项目
    print("\n4️⃣ 提取岗位列表...")
    jobs = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('*').forEach(el => {
            const text = (el.innerText || '').trim();
            if (text.length > 15 && text.length < 200) {
                result.push(text);
            }
        });
        return result;
    }''')
    
    # 筛选可能包含岗位信息的文本
    job_items = [j for j in jobs if any(kw in j for kw in ['Python', '开发', '数据', '爬虫', '自动化', '工程师', '远程', '兼职', '元/月', '元/天', '预算'])]
    
    print(f"找到 {len(job_items)} 个相关岗位:")
    for i, job in enumerate(job_items[:20], 1):
        print(f"{i}. {job[:150]}")
    
    # 保存所有文本到文件
    with open('/root/.openclaw/workspace/proginn_job_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(jobs[:100]))
    print(f"\n💾 已保存前 100 条内容到 proginn_job_list.txt")
    
    browser.close()
    
except Exception as e:
    print(f"❌ 错误：{e}")
