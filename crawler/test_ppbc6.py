#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析PPBC搜索页面的HTML结构
"""

import requests
from urllib.parse import quote

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
})

def analyze_page():
    urls_to_check = [
        "https://ppbc.iplant.cn/list21?keyword=银杏",
        "https://mpb.iplant.cn/list?latin=Ginkgo%20biloba",
        "https://ppbc.iplant.cn/sp/31602",
    ]
    
    for url in urls_to_check:
        print("=" * 80)
        print(f"URL: {url}")
        print("=" * 80)
        
        response = session.get(url, timeout=30)
        content = response.text
        
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(content)}")
        print()
        
        print("HTML内容（前2000字符）:")
        print(content[:2000])
        print("\n" + "=" * 80 + "\n")
        
        with open(f'/tmp/ppbc_{url.replace("/", "_").replace("?", "_").replace(":", "_")}.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已保存完整内容到临时文件")
        print()

if __name__ == '__main__':
    analyze_page()
