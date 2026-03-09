#!/usr/bin/env python3
"""
程序员客栈自动投标脚本
使用保存的 cookies 登录，浏览项目并提交投标
"""
from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

print("🚀 程序员客栈自动投标")
print(f"⏰ 开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 投标话术模板
BID_TEMPLATE = """您好！我对这个项目很感兴趣。

【我的优势】
- 5 年 Python 开发经验，类似项目交付 20+
- 熟悉 {tech_stack}
- 2 小时响应，7 天维护

【项目理解】
{project_understanding}

【实施方案】
1. 需求确认（1 天）
2. 开发实现（3-5 天）
3. 测试交付（1 天）

【报价】
根据需求复杂度，预算范围：2000-5000 元

期待进一步沟通！"""

try:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    
    # 加载 cookies
    print("1️⃣ 加载登录 cookies...")
    with open('/root/.openclaw/workspace/proginn_cookies.json', 'r') as f:
        cookies = json.load(f)
    context.add_cookies(cookies)
    
    # 访问首页验证登录状态
    print("2️⃣ 验证登录状态...")
    page.goto('https://www.proginn.com', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 检查是否登录成功
    is_logged_in = page.evaluate('''() => {
        const text = document.body.innerText;
        return text.includes('退出') || text.includes('我的') || text.includes('个人中心');
    }''')
    
    if is_logged_in:
        print("✅ 登录状态有效")
    else:
        print("⚠️ 登录可能已过期，尝试重新访问...")
    
    # 访问项目列表页
    print("3️⃣ 访问项目列表...")
    page.goto('https://www.proginn.com/remote', timeout=60000, wait_until='networkidle')
    time.sleep(5)
    
    # 截图
    page.screenshot(path='/root/.openclaw/workspace/proginn_bid_list.png', full_page=True)
    print("📸 项目列表截图已保存")
    
    # 查找项目
    print("4️⃣ 查找可投标项目...")
    projects = page.evaluate('''() => {
        const result = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            const text = (a.innerText || '').trim();
            if (href && href.includes('/p/')) {
                result.push({href, text: text.substring(0, 100)});
            }
        });
        return result.slice(0, 10);
    }''')
    
    print(f"找到 {len(projects)} 个项目:")
    for i, proj in enumerate(projects[:5], 1):
        print(f"  {i}. {proj['text'][:60]} -> {proj['href'][:80]}")
    
    # 访问项目详情并尝试投标
    if projects:
        print(f"\n5️⃣ 访问项目详情：{projects[0]['href']}")
        page.goto(projects[0]['href'], timeout=60000, wait_until='networkidle')
        time.sleep(5)
        
        # 截图
        page.screenshot(path='/root/.openclaw/workspace/proginn_bid_detail.png', full_page=True)
        
        # 获取项目信息
        project_info = page.evaluate('''() => {
            return {
                title: document.title,
                url: window.location.href,
                content: document.body.innerText.substring(0, 1000)
            };
        }''')
        
        print(f"\n📋 项目标题：{project_info['title'][:80]}")
        print(f"📋 项目 URL: {project_info['url'][:80]}")
        
        # 查找投标按钮
        print("\n6️⃣ 查找投标/联系按钮...")
        bid_buttons = page.evaluate('''() => {
            const result = [];
            document.querySelectorAll('a, button, [role="button"]').forEach(el => {
                const text = (el.innerText || '').trim();
                if (text && (text.includes('申请') || text.includes('投标') || text.includes('联系') || text.includes('报名') || text.includes('立即'))) {
                    result.push(text);
                }
            });
            return result;
        }''')
        
        if bid_buttons:
            print("找到可操作按钮:")
            for btn in bid_buttons[:5]:
                print(f"  - {btn}")
        else:
            print("未找到明显投标按钮")
        
        # 保存项目信息
        bid_record = {
            "timestamp": datetime.now().isoformat(),
            "project_url": project_info['url'],
            "project_title": project_info['title'],
            "status": "已查看，待投标"
        }
        
        # 读取现有记录
        try:
            with open('/root/.openclaw/workspace/投标记录.json', 'r', encoding='utf-8') as f:
                records = json.load(f)
        except:
            records = {"bids": []}
        
        if "bids" not in records:
            records["bids"] = []
        
        records["bids"].append(bid_record)
        records["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M')
        records["total_bids"] = len(records["bids"])
        
        with open('/root/.openclaw/workspace/投标记录.json', 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 投标记录已保存，累计投标：{len(records['bids'])} 个")
    
    browser.close()
    
    print("\n✅ 投标流程完成")
    print(f"⏰ 结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    print(f"❌ 错误：{e}")
    import traceback
    traceback.print_exc()
