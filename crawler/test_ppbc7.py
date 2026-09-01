#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试从mpb.iplant.cn获取图片
"""

import requests
import re
from urllib.parse import quote

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://mpb.iplant.cn/'
})

def test_mpb():
    latin_name = "Ginkgo biloba"
    encoded_latin = quote(latin_name)
    search_url = f"https://mpb.iplant.cn/list?latin={encoded_latin}"
    
    print(f"搜索: {latin_name}")
    print(f"URL: {search_url}")
    print()
    
    response = session.get(search_url, timeout=30)
    content = response.text
    
    print(f"状态码: {response.status_code}")
    print(f"内容长度: {len(response.text)}")
    print()
    
    img_pattern = r'//img\d+\.iplant\.cn/image\d+/\d+/[A-F0-9]+\.(?:jpg|jpeg|png)'
    img_matches = re.findall(img_pattern, content, re.IGNORECASE)
    unique_imgs = list(dict.fromkeys(img_matches))
    
    print(f"找到 {len(unique_imgs)} 个图片URL")
    for i, img_url in enumerate(unique_imgs[:5]):
        full_url = f"https:{img_url}"
        print(f"  [{i}] {full_url}")
        
        response = session.get(full_url, timeout=30)
        print(f"      状态码: {response.status_code}, 大小: {len(response.content)} 字节")
        
        if len(response.content) > 10000:
            with open(f'/tmp/test_img_{i}.jpg', 'wb') as f:
                f.write(response.content)
            print(f"      ✓ 已保存到 /tmp/test_img_{i}.jpg")
    
    print()
    print("=" * 60)
    print("访问tu页面获取大图...")
    
    tu_pattern = r'/tu/(\d+)'
    tu_matches = re.findall(tu_pattern, content)
    unique_tu = list(dict.fromkeys(tu_matches))
    
    print(f"找到 {len(unique_tu)} 个tu页面")
    for tu_id in unique_tu[:3]:
        tu_url = f"https://ppbc.iplant.cn/tu/{tu_id}"
        print(f"\n  访问: {tu_url}")
        
        response = session.get(tu_url, timeout=30)
        tu_content = response.text
        
        big_img_pattern = r'//img\d+\.iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)'
        big_img_matches = re.findall(big_img_pattern, tu_content, re.IGNORECASE)
        unique_big = list(dict.fromkeys(big_img_matches))
        
        for img_url in unique_big[:2]:
            if 'thumb' in img_url.lower() or 'small' in img_url.lower():
                continue
            full_url = f"https:{img_url}"
            print(f"    大图URL: {full_url}")
            
            response = session.get(full_url, timeout=30)
            print(f"    状态码: {response.status_code}, 大小: {len(response.content)} 字节")
            
            if len(response.content) > 10000:
                with_open = open(f'/tmp/test_tu_{tu_id}.jpg', 'wb')
                with_open.write(response.content)
                with_open.close()
                print(f"    ✓ 已保存到 /tmp/test_tu_{tu_id}.jpg")
                break

if __name__ == '__main__':
    test_mpb()
