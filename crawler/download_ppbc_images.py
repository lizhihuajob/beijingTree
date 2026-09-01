#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPBC中国植物图像库图片下载脚本
使用正确的URL格式从ppbc.iplant.cn获取图片
"""

import json
import os
import re
import time
import requests
from urllib.parse import quote
from pathlib import Path

class PPBCImageDownloader:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.frontend_dir = self.base_dir / 'frontend'
        self.public_dir = self.frontend_dir / 'public'
        self.images_dir = self.public_dir / 'images' / 'plants'
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://ppbc.iplant.cn/'
        })
        
        self.failed_downloads = []
        self.success_count = 0
    
    def search_plant(self, plant_name):
        """搜索植物，获取图片页面链接"""
        try:
            encoded_name = quote(plant_name)
            search_url = f"https://ppbc.iplant.cn/list21?keyword={encoded_name}"
            
            response = self.session.get(search_url, timeout=30)
            if response.status_code != 200:
                return None
            
            content = response.text
            
            img_patterns = [
                r'//img\d+\.iplant\.cn/(?:image|photo)[^"\'\s<>]*\.(?:jpg|jpeg|png)',
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if 'thumb' not in match.lower() and 'small' not in match.lower():
                            return 'https:' + match if not match.startswith('http') else match
            
            tu_patterns = [
                r'/tu/\d+',
            ]
            
            for pattern in tu_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    return f"https://ppbc.iplant.cn{matches[0]}"
            
            return None
        except Exception as e:
            return None
    
    def get_image_from_tu_page(self, page_url):
        """从tu页面获取图片URL"""
        try:
            response = self.session.get(page_url, timeout=30)
            if response.status_code != 200:
                return None
            
            content = response.text
            
            img_patterns = [
                r'//img\d+\.iplant\.cn/(?:image|photo)[^"\'\s<>]*\.(?:jpg|jpeg|png)',
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if 'thumb' not in match.lower() and 'small' not in match.lower():
                            return 'https:' + match if not match.startswith('http') else match
            
            return None
        except Exception as e:
            return None
    
    def download_image(self, url, save_path):
        """下载图片"""
        try:
            if url.startswith('//'):
                url = 'https:' + url
            
            response = self.session.get(url, timeout=30)
            if response.status_code == 200 and len(response.content) > 5000:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            pass
        return False
    
    def try_multiple_servers(self, plant_name, save_path):
        """尝试从多个图片服务器获取图片"""
        image_url = self.search_plant(plant_name)
        
        if not image_url:
            return False
        
        if image_url.startswith('https://ppbc.iplant.cn/tu/'):
            image_url = self.get_image_from_tu_page(image_url)
            if not image_url:
                return False
        
        return self.download_image(image_url, save_path)
    
    def download_all_plants(self, plants_data, max_plants=None):
        """下载所有植物的图片"""
        total = len(plants_data) if max_plants is None else min(len(plants_data), max_plants)
        print(f"开始下载图片，共 {total} 种植物...")
        print(f"图片将保存到: {self.images_dir}")
        print("-" * 60)
        
        processed = 0
        for i, plant in enumerate(plants_data, 1):
            if max_plants and processed >= max_plants:
                break
            
            name_cn = plant.get('name_cn', '')
            if not name_cn:
                continue
            
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', name_cn)
            image_path = self.images_dir / f"{safe_name}.jpg"
            
            if image_path.exists() and image_path.stat().st_size > 5000:
                print(f"[{i}/{len(plants_data)}] {name_cn} - 已存在 ✓")
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'PPBC中国植物图像库'
                self.success_count += 1
                processed += 1
                continue
            
            print(f"[{i}/{len(plants_data)}] {name_cn} - 搜索中...", end='', flush=True)
            
            if self.try_multiple_servers(name_cn, image_path):
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'PPBC中国植物图像库'
                self.success_count += 1
                print(f" 下载成功 ✓")
            else:
                common_names = plant.get('common_names', [])
                alt_success = False
                for alt_name in common_names[:2]:
                    if self.try_multiple_servers(alt_name, image_path):
                        plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                        plant['image_urls'] = [plant['primary_image']]
                        plant['image_source'] = 'PPBC中国植物图像库'
                        self.success_count += 1
                        print(f"  (别名) 下载成功 ✓")
                        alt_success = True
                        break
                
                if not alt_success:
                    seed = name_cn.replace(' ', '')
                    plant['primary_image'] = f"https://picsum.photos/seed/{seed}/800/600"
                    plant['image_urls'] = [plant['primary_image']]
                    plant['image_source'] = 'picsum.photos'
                    self.failed_downloads.append(name_cn)
                    print(f"  未找到")
            
            processed += 1
            time.sleep(0.3)
        
        print("-" * 60)
        print(f"下载完成! 成功: {self.success_count}/{total}")
        if self.failed_downloads:
            print(f"未找到图片的植物: {len(self.failed_downloads)} 种")
            for name in self.failed_downloads[:15]:
                print(f"  - {name}")
            if len(self.failed_downloads) > 15:
                print(f"  ... 还有 {len(self.failed_downloads)-15} 种")
        
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
    print("PPBC中国植物图像库图片下载工具")
    print("=" * 60)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    plants = data.get('plants', [])
    print(f"\n加载植物数据: {len(plants)} 种")
    
    downloader = PPBCImageDownloader(base_dir)
    updated_plants = downloader.download_all_plants(plants)
    
    data['plants'] = updated_plants
    data['metadata']['image_count'] = downloader.success_count
    data['metadata']['image_downloaded_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    downloader.save_updated_data(data, data_file)
    
    print("=" * 60)
    print("图片下载完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
