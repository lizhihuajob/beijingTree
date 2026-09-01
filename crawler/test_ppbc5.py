#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新版PPBC图片下载器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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

def search_species_by_name(name_cn):
    """通过中文名搜索物种页面"""
    encoded_name = quote(name_cn)
    search_url = f"https://ppbc.iplant.cn/list21?keyword={encoded_name}"
    
    print(f"搜索: {name_cn}")
    print(f"URL: {search_url}")
    print()
    
    response = session.get(search_url, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"内容长度: {len(response.text)}")
    
    content = response.text
    
    sp_pattern = r'/sp/(\d+)'
    sp_matches = re.findall(sp_pattern, content)
    print(f"\n找到 sp ID: {list(dict.fromkeys(sp_matches))[:5]}")
    
    tu_pattern = r'/tu/(\d+)'
    tu_matches = re.findall(tu_pattern, content)
    print(f"找到 tu ID: {list(dict.fromkeys(tu_matches))[:5]}")
    
    if sp_matches:
        return ('sp', list(dict.fromkeys(sp_matches))[0])
    elif tu_matches:
        return ('tu', list(dict.fromkeys(tu_matches))[0])
    return None

def get_image_from_sp(sp_id):
    """从sp页面获取图片"""
    sp_url = f"https://ppbc.iplant.cn/sp/{sp_id}"
    print(f"\n访问sp页面: {sp_url}")
    
    response = session.get(sp_url, timeout=30)
    print(f"状态码: {response.status_code}")
    
    content = response.text
    
    img_pattern = r'img\d+\.iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)'
    matches = re.findall(img_pattern, content, re.IGNORECASE)
    unique_matches = list(dict.fromkeys(matches))
    print(f"找到图片URL: {unique_matches[:5]}")
    
    if unique_matches:
        return f"https://{unique_matches[0]}"
    return None

def download_image(url, save_path):
    """下载图片"""
    print(f"\n下载: {url}")
    response = session.get(url, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"内容长度: {len(response.content)} 字节")
    
    if len(response.content) > 10000:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ 已保存到 {save_path}")
        return True
    return False

def test():
    test_plants = [
        '月季',
        '银杏',
        '水杉',
        '牡丹',
        '桂花',
    ]
    
    for plant in test_plants:
        print("\n" + "=" * 60)
        print(f"测试植物: {plant}")
        print("=" * 60)
        
        result = search_species_by_name(plant)
        if result:
            type_id, id_value = result
            if type_id == 'sp':
                image_url = get_image_from_sp(id_value)
                if image_url:
                    save_path = f'/tmp/{plant}.jpg'
                    download_image(image_url, save_path)
            else:
                print(f"需要从tu页面获取图片...")
        else:
            print("未找到物种页面")

if __name__ == '__main__':
    test()
