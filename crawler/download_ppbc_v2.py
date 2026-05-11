#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPBC中国植物图像库图片下载脚本
通过拉丁学名搜索物种页面，然后获取图片URL
"""

import json
import os
import re
import time
import requests
from urllib.parse import quote
from pathlib import Path

class PPBCImageDownloaderV2:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.frontend_dir = self.base_dir / 'frontend'
        self.public_dir = self.frontend_dir / 'public'
        self.images_dir = self.public_dir / 'images' / 'plants'
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://ppbc.iplant.cn/'
        })
        
        self.failed_downloads = []
        self.success_count = 0
        self.name_to_sp_id = {}
    
    def search_species_by_latin(self, latin_name):
        """通过拉丁学名搜索物种页面"""
        try:
            encoded_name = quote(latin_name)
            search_urls = [
                f"https://ppbc.iplant.cn/list21?keyword={encoded_name}",
                f"https://mpb.iplant.cn/list?latin={encoded_name}",
            ]
            
            for url in search_urls:
                response = self.session.get(url, timeout=30)
                if response.status_code != 200:
                    continue
                
                content = response.text
                
                sp_pattern = r'/sp/(\d+)'
                sp_matches = re.findall(sp_pattern, content)
                if sp_matches:
                    unique_sp = list(dict.fromkeys(sp_matches))
                    return unique_sp[0]
                
                tu_pattern = r'/tu/(\d+)'
                tu_matches = re.findall(tu_pattern, content)
                if tu_matches:
                    return f"tu_{tu_matches[0]}"
            
            return None
        except Exception as e:
            return None
    
    def search_species_by_name(self, name_cn):
        """通过中文名搜索物种页面"""
        try:
            encoded_name = quote(name_cn)
            search_url = f"https://ppbc.iplant.cn/list21?keyword={encoded_name}"
            
            response = self.session.get(search_url, timeout=30)
            if response.status_code != 200:
                return None
            
            content = response.text
            
            sp_pattern = r'/sp/(\d+)'
            sp_matches = re.findall(sp_pattern, content)
            if sp_matches:
                unique_sp = list(dict.fromkeys(sp_matches))
                return unique_sp[0]
            
            tu_pattern = r'/tu/(\d+)'
            tu_matches = re.findall(tu_pattern, content)
            if tu_matches:
                return f"tu_{tu_matches[0]}"
            
            return None
        except Exception as e:
            return None
    
    def get_image_url_from_sp(self, sp_id):
        """从物种页面获取图片URL"""
        try:
            if sp_id.startswith('tu_'):
                tu_id = sp_id[3:]
                return self.get_image_url_from_tu(tu_id)
            
            sp_url = f"https://ppbc.iplant.cn/sp/{sp_id}"
            response = self.session.get(sp_url, timeout=30)
            if response.status_code != 200:
                return None
            
            content = response.text
            
            img_pattern = r'img\d+\.iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            if matches:
                unique_matches = list(dict.fromkeys(matches))
                for match in unique_matches:
                    if 'thumb' not in match.lower() and 'small' not in match.lower():
                        return f"https://{match}"
            
            tu_pattern = r'/tu/(\d+)'
            tu_matches = re.findall(tu_pattern, content)
            if tu_matches:
                return self.get_image_url_from_tu(tu_matches[0])
            
            return None
        except Exception as e:
            return None
    
    def get_image_url_from_tu(self, tu_id):
        """从tu页面获取图片URL"""
        try:
            tu_url = f"https://ppbc.iplant.cn/tu/{tu_id}"
            response = self.session.get(tu_url, timeout=30)
            if response.status_code != 200:
                return None
            
            content = response.text
            
            img_pattern = r'img\d+\.iplant\.cn/[^"\'\s<>]+\.(?:jpg|jpeg|png)'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            if matches:
                unique_matches = list(dict.fromkeys(matches))
                for match in unique_matches:
                    if 'thumb' not in match.lower() and 'small' not in match.lower():
                        return f"https://{match}"
            
            return None
        except Exception as e:
            return None
    
    def download_image(self, url, save_path):
        """下载图片"""
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200 and len(response.content) > 10000:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            pass
        return False
    
    def get_image_for_plant(self, plant):
        """为单个植物获取图片"""
        name_cn = plant.get('name_cn', '')
        name_latin = plant.get('name_latin', '')
        
        if not name_cn:
            return None
        
        safe_name = re.sub(r'[\\/:*?"<>|]', '_', name_cn)
        image_path = self.images_dir / f"{safe_name}.jpg"
        
        if image_path.exists() and image_path.stat().st_size > 10000:
            return image_path
        
        sp_id = None
        
        if name_latin:
            sp_id = self.search_species_by_latin(name_latin)
        
        if not sp_id:
            sp_id = self.search_species_by_name(name_cn)
        
        if not sp_id:
            return None
        
        image_url = self.get_image_url_from_sp(sp_id)
        
        if not image_url:
            return None
        
        if self.download_image(image_url, image_path):
            return image_path
        
        return None
    
    def download_all_plants(self, plants_data, max_plants=None):
        """下载所有植物的图片"""
        total = len(plants_data) if max_plants is None else min(len(plants_data), max_plants)
        print(f"开始下载图片，共 {total} 种植物...")
        print(f"图片将保存到: {self.images_dir}")
        print("-" * 60)
        
        for i, plant in enumerate(plants_data, 1):
            if max_plants and i > max_plants:
                break
            
            name_cn = plant.get('name_cn', '')
            if not name_cn:
                continue
            
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', name_cn)
            image_path = self.images_dir / f"{safe_name}.jpg"
            
            if image_path.exists() and image_path.stat().st_size > 10000:
                print(f"[{i}/{len(plants_data)}] {name_cn} - 已存在 ✓")
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'PPBC中国植物图像库'
                self.success_count += 1
                continue
            
            print(f"[{i}/{len(plants_data)}] {name_cn} - 搜索中...", end='', flush=True)
            
            saved_path = self.get_image_for_plant(plant)
            
            if saved_path:
                plant['primary_image'] = f"/images/plants/{safe_name}.jpg"
                plant['image_urls'] = [plant['primary_image']]
                plant['image_source'] = 'PPBC中国植物图像库'
                self.success_count += 1
                print(f"  下载成功 ✓")
            else:
                common_names = plant.get('common_names', [])
                alt_success = False
                for alt_name in common_names[:3]:
                    temp_plant = {'name_cn': alt_name, 'name_latin': plant.get('name_latin', '')}
                    alt_path = self.get_image_for_plant(temp_plant)
                    if alt_path:
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
            
            time.sleep(0.5)
        
        print("-" * 60)
        print(f"下载完成! 成功: {self.success_count}/{total}")
        if self.failed_downloads:
            print(f"未找到图片的植物: {len(self.failed_downloads)} 种")
            for name in self.failed_downloads[:20]:
                print(f"  - {name}")
            if len(self.failed_downloads) > 20:
                print(f"  ... 还有 {len(self.failed_downloads)-20} 种")
        
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
    print("PPBC中国植物图像库图片下载工具 V2")
    print("=" * 60)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    plants = data.get('plants', [])
    print(f"\n加载植物数据: {len(plants)} 种")
    
    downloader = PPBCImageDownloaderV2(base_dir)
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
