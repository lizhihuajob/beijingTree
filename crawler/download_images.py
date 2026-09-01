#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
植物图片下载脚本
从PPBC中国植物图像库搜索并下载植物真实图片
"""

import json
import os
import re
import time
import requests
from urllib.parse import quote
from pathlib import Path

class PlantImageDownloader:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.frontend_dir = self.base_dir / 'frontend'
        self.public_dir = self.frontend_dir / 'public'
        self.images_dir = self.public_dir / 'images' / 'plants'
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        })
        
        self.failed_downloads = []
        self.success_count = 0
    
    def download_image(self, url, save_path):
        """下载图片"""
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            pass
        return False
    
    def search_ppbc(self, plant_name):
        """搜索PPBC获取植物图片"""
        try:
            encoded_name = quote(plant_name)
            search_url = f"https://ppbc.iplant.cn/tu/{encoded_name}"
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                content = response.text
                
                img_patterns = [
                    r'https?://img\d+\.iplant\.cn/[^"\'<>]+\.(?:jpg|jpeg|png)',
                    r'https?://[^"\'<>]+\.plantphoto\.cn/[^"\'<>]+\.(?:jpg|jpeg|png)',
                ]
                
                for pattern in img_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        return matches[0]
            
            return None
        except Exception as e:
            return None
    
    def download_plant_images(self, plants_data):
        """下载所有植物的图片"""
        print(f"开始下载图片，共 {len(plants_data)} 种植物...")
        print(f"图片将保存到: {self.images_dir}")
        print("-" * 60)
        
        for i, plant in enumerate(plants_data, 1):
            name_cn = plant.get('name_cn', '')
            if not name_cn:
                continue
            
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', name_cn)
            image_path = self.images_dir / f"{safe_name}.jpg"
            
            if image_path.exists() and image_path.stat().st_size > 1000:
                print(f"[{i}/{len(plants_data)}] {name_cn} - 已存在 ✓")
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = '本地图片'
                self.success_count += 1
                continue
            
            print(f"[{i}/{len(plants_data)}] {name_cn} - 搜索中...", end='', flush=True)
            
            image_url = None
            
            if plant.get('ppbc_id'):
                ppbc_id = plant['ppbc_id']
                test_urls = [
                    f"https://img1.iplant.cn/image2/b/{ppbc_id}.jpg",
                    f"https://img2.iplant.cn/image2/b/{ppbc_id}.jpg",
                    f"https://img.plantphoto.cn/image2/b/{ppbc_id}.jpg",
                ]
                for url in test_urls:
                    if self.download_image(url, image_path):
                        image_url = url
                        break
            
            if not image_url:
                image_url = self.search_ppbc(name_cn)
                if image_url:
                    if not self.download_image(image_url, image_path):
                        image_url = None
            
            if image_url and image_path.exists() and image_path.stat().st_size > 1000:
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'PPBC中国植物图像库'
                self.success_count += 1
                print(f" 下载成功 ✓")
            else:
                seed = name_cn.replace(' ', '')
                plant['primary_image'] = f"https://picsum.photos/seed/{seed}/800/600"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'picsum.photos'
                self.failed_downloads.append(name_cn)
                print(f" 未找到真实图片，使用备用图片")
            
            time.sleep(0.5)
        
        print("-" * 60)
        print(f"下载完成! 成功: {self.success_count}/{len(plants_data)}")
        if self.failed_downloads:
            print(f"未找到真实图片的植物: {len(self.failed_downloads)} 种")
            for name in self.failed_downloads[:10]:
                print(f"  - {name}")
            if len(self.failed_downloads) > 10:
                print(f"  ... 还有 {len(self.failed_downloads)-10} 种")
        
        return plants_data
    
    def save_updated_data(self, data, output_path):
        """保存更新后的数据"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到: {output_path}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    data_file = os.path.join(base_dir, 'frontend', 'src', 'data', 'plants.json')
    
    print("=" * 60)
    print("北京植物园植物图片下载工具")
    print("=" * 60)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    plants = data.get('plants', [])
    print(f"\n加载植物数据: {len(plants)} 种")
    
    downloader = PlantImageDownloader(base_dir)
    updated_plants = downloader.download_plant_images(plants)
    
    data['plants'] = updated_plants
    data['metadata']['image_count'] = downloader.success_count
    data['metadata']['image_downloaded_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    downloader.save_updated_data(data, data_file)
    
    print("=" * 60)
    print("图片下载完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
