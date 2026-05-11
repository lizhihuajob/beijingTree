#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试V3下载脚本 - 下载前20种植物
"""

import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from download_ppbc_v3 import PPBCImageDownloaderV3

def test():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, 'frontend', 'src', 'data', 'plants.json')
    
    print("=" * 60)
    print("测试PPBC图片下载工具 V3")
    print("=" * 60)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    plants = data.get('plants', [])
    print(f"\n总植物数量: {len(plants)}")
    print(f"测试下载前20种植物...\n")
    
    test_plants = plants[:20]
    
    downloader = PPBCImageDownloaderV3(base_dir)
    updated_plants = downloader.download_all_plants(test_plants)
    
    print("\n测试结果:")
    for i, plant in enumerate(updated_plants):
        print(f"  [{i+1}] {plant['name_cn']}: {plant['image_source']}")
        if plant['image_source'] == 'PPBC中国植物图像库':
            print(f"       图片路径: {plant['primary_image']}")

if __name__ == '__main__':
    test()
