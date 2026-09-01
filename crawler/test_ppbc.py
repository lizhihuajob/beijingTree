#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PPBC图片下载
"""

import requests
import re
from urllib.parse import quote

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://ppbc.iplant.cn/'
})

def test_search():
    plant_name = "月季"
    encoded_name = quote(plant_name)
    search_url = f"https://ppbc.iplant.cn/list21?keyword={encoded_name}"
    
    print(f"搜索: {plant_name}")
    print(f"URL: {search_url}")
    print()
    
    response = session.get(search_url, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"内容长度: {len(response.text)} 字符")
    print()
    
    content = response.text
    
    print("=" * 60)
    print("查找图片URL...")
    
    img_patterns = [
        r'//img\d+\.iplant\.cn/(?:image|photo)[^"\'\s<>]*\.(?:jpg|jpeg|png)',
    ]
    
    for pattern in img_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        print(f"\nPattern: {pattern}")
        print(f"找到 {len(matches)} 个匹配")
        if matches:
            unique_matches = list(dict.fromkeys(matches))
            for i, match in enumerate(unique_matches[:10]):
                print(f"  [{i}] {match}")
    
    print()
    print("=" * 60)
    print("查找tu页面链接...")
    
    tu_pattern = r'/tu/\d+'
    tu_matches = re.findall(tu_pattern, content)
    print(f"找到 {len(tu_matches)} 个tu页面")
    unique_tu = list(dict.fromkeys(tu_matches))
    for i, tu in enumerate(unique_tu[:5]):
        print(f"  [{i}] {tu}")

if __name__ == '__main__':
    test_search()
