#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PPBC图片搜索 - 查看sp页面内容
"""

import requests
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
})

def test_sp_page():
    urls = [
        "https://ppbc.iplant.cn/sp/18357",
        "https://ppbc.iplant.cn/tu/1761293",
    ]
    
    for url in urls:
        print("=" * 80)
        print(f"URL: {url}")
        print("=" * 80)
        
        try:
            response = session.get(url, timeout=30)
            content = response.text
            
            print(f"状态码: {response.status_code}")
            print(f"内容长度: {len(content)}")
            print()
            
            img_patterns = [
                r'img\d+\.iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)',
                r'iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)',
                r'/tu/\d+',
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    unique_matches = list(dict.fromkeys(matches))[:20]
                    print(f"Pattern '{pattern}' 找到 {len(unique_matches)} 个:")
                    for i, m in enumerate(unique_matches):
                        print(f"  [{i}] {m}")
                    print()
            
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
        
        print()

if __name__ == '__main__':
    test_sp_page()
