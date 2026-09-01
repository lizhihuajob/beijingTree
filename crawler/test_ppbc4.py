#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PPBC图片下载
"""

import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://ppbc.iplant.cn/'
})

def test_download():
    image_url = "https://img3.iplant.cn/image61/b/39E0657C8791D5BF.jpg"
    
    print(f"尝试下载: {image_url}")
    
    try:
        response = session.get(image_url, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.content)} 字节")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        
        if len(response.content) > 1000:
            with open('/tmp/test_image.jpg', 'wb') as f:
                f.write(response.content)
            print(f"✓ 图片已保存到 /tmp/test_image.jpg")
        else:
            print(f"✗ 图片太小，可能不是有效图片")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_download()
