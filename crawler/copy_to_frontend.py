#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将最终数据复制到前端
"""

import json
import os

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(base_dir, '..', 'data', 'plants_final.json')
    target_file = os.path.join(base_dir, '..', 'frontend', 'src', 'data', 'plants.json')
    
    print(f"从 {source_file} 读取数据...")
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"数据包含 {data['metadata']['total_count']} 种植物")
    print(f"其中 {data['metadata']['ppbc_image_count']} 种使用PPBC真实图片")
    
    print(f"写入到 {target_file} ...")
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("完成！")
    
if __name__ == '__main__':
    main()
