#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PPBC图片搜索
"""

import requests
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
    
    urls_to_try = [
        f"https://ppbc.iplant.cn/list21?keyword={encoded_name}",
        f"https://ppbc.iplant.cn/tu/{encoded_name}",
        f"https://mpb.iplant.cn/list?latin=Rosa%20chinensis",
        f"https://ppbc.iplant.cn/sp/18357",
    ]
    
    for url in urls_to_try:
        print("=" * 60)
        print(f"URL: {url}")
        try:
            response = session.get(url, timeout=30)
            print(f"状态码: {response.status_code}")
            print(f"内容长度: {len(response.text)}")
            print(f"内容前500字符:")
            print(response.text[:500])
        except Exception as e:
            print(f"错误: {e}")
        print()

if __name__ == '__main__':
    test_search()
