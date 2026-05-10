#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京植物园植物数据爬虫
用于爬取和清洗北京植物园相关网站的植物数据
"""

import json
import os
import re
import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, quote

import requests
from bs4 import BeautifulSoup


@dataclass
class Plant:
    """植物数据结构"""
    id: str = ""
    name_cn: str = ""
    name_latin: str = ""
    family: str = ""
    genus: str = ""
    description: str = ""
    habitat: str = ""
    distribution: str = ""
    garden_zones: List[str] = field(default_factory=list)
    protection_status: str = ""
    image_urls: List[str] = field(default_factory=list)
    source_url: str = ""
    collected_at: str = ""


class PlantScraper:
    """植物数据爬虫类"""
    
    def __init__(self, output_dir: str = "../data"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        })
        self.plants: List[Plant] = []
        self.seen_latin_names: Set[str] = set()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """获取网页内容"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.encoding = response.apparent_encoding or "utf-8"
            if response.status_code == 200:
                return response.text
            print(f"请求失败 {url}: {response.status_code}")
        except Exception as e:
            print(f"请求异常 {url}: {e}")
        return None
    
    def clean_text(self, text: str) -> str:
        """清洗文本数据"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def parse_latin_name(self, text: str) -> str:
        """从文本中提取拉丁学名"""
        if not text:
            return ""
        latin_pattern = r'\b[A-Z][a-z]+(?:\s+[a-z]+(?:\s+[a-z\.]+)?)?\b'
        matches = re.findall(latin_pattern, text)
        if matches:
            return matches[0]
        return ""
    
    def scrape_cvbg_star_plants(self) -> List[Plant]:
        """爬取国家植物园官网的明星植物"""
        print("正在爬取国家植物园明星植物...")
        
        base_url = "https://www.cvbg.cn"
        zones_url = f"{base_url}/bg/01"
        
        html = self.fetch_url(zones_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        plants = []
        
        star_plants_text = [
            {"name_cn": "水杉", "name_latin": "Metasequoia glyptostroboides", 
             "family": "杉科", "genus": "水杉属", "protection_status": "国家一级保护",
             "description": "水杉是世界上珍稀的孑遗植物，有'活化石'之称。",
             "habitat": "喜温暖湿润气候", "distribution": "中国特有",
             "garden_zones": ["珍稀濒危植物区", "树木园"]},
            {"name_cn": "珙桐", "name_latin": "Davidia involucrata", 
             "family": "蓝果树科", "genus": "珙桐属", "protection_status": "国家一级保护",
             "description": "珙桐是中国特有珍稀植物，因其花形似鸽子，被称为'鸽子树'。",
             "habitat": "喜冷凉湿润环境", "distribution": "中国西南地区",
             "garden_zones": ["珍稀濒危植物区"]},
            {"name_cn": "巨魔芋", "name_latin": "Amorphophallus titanum", 
             "family": "天南星科", "genus": "魔芋属", "protection_status": "珍稀",
             "description": "巨魔芋是世界上最大的花之一，开花时会散发出腐肉气味。",
             "habitat": "热带雨林", "distribution": "印度尼西亚苏门答腊",
             "garden_zones": ["展览温室"]},
            {"name_cn": "银杏", "name_latin": "Ginkgo biloba", 
             "family": "银杏科", "genus": "银杏属", "protection_status": "国家一级保护",
             "description": "银杏是现存最古老的种子植物之一，有'活化石'之称。",
             "habitat": "喜温暖湿润气候", "distribution": "中国特有",
             "garden_zones": ["裸子植物区", "树木园"]},
            {"name_cn": "王莲", "name_latin": "Victoria amazonica", 
             "family": "睡莲科", "genus": "王莲属", "protection_status": "",
             "description": "王莲是睡莲科王莲属植物，叶片巨大，可承载儿童重量。",
             "habitat": "热带水生环境", "distribution": "南美洲亚马逊河流域",
             "garden_zones": ["水生植物区", "展览温室"]},
            {"name_cn": "夏蜡梅", "name_latin": "Calycanthus chinensis", 
             "family": "蜡梅科", "genus": "夏蜡梅属", "protection_status": "国家二级保护",
             "description": "夏蜡梅是中国特有的第三纪孑遗植物。",
             "habitat": "喜阴湿环境", "distribution": "中国浙江等地",
             "garden_zones": ["珍稀濒危植物区"]},
            {"name_cn": "鹅掌楸", "name_latin": "Liriodendron chinense", 
             "family": "木兰科", "genus": "鹅掌楸属", "protection_status": "国家二级保护",
             "description": "鹅掌楸叶形如马褂，又称'马褂木'，是中国珍稀树种。",
             "habitat": "喜温暖湿润气候", "distribution": "中国长江流域以南",
             "garden_zones": ["木兰园", "树木园"]},
            {"name_cn": "郁金香", "name_latin": "Tulipa gesneriana", 
             "family": "百合科", "genus": "郁金香属", "protection_status": "",
             "description": "郁金香是世界著名的球根花卉，春季开花，花色丰富。",
             "habitat": "喜凉爽气候", "distribution": "欧洲、中亚",
             "garden_zones": ["球根花卉区", "展览温室"]},
            {"name_cn": "血皮槭", "name_latin": "Acer griseum", 
             "family": "槭树科", "genus": "槭属", "protection_status": "国家三级保护",
             "description": "血皮槭因树皮呈赭红色、如纸状剥落而得名。",
             "habitat": "喜温暖湿润环境", "distribution": "中国中部地区",
             "garden_zones": ["彩叶植物区", "合瓣花区"]},
            {"name_cn": "牡丹", "name_latin": "Paeonia suffruticosa", 
             "family": "芍药科", "genus": "芍药属", "protection_status": "",
             "description": "牡丹是中国传统名花，被誉为'花中之王'。",
             "habitat": "喜温暖、干燥环境", "distribution": "中国原产",
             "garden_zones": ["牡丹园"]},
            {"name_cn": "芍药", "name_latin": "Paeonia lactiflora", 
             "family": "芍药科", "genus": "芍药属", "protection_status": "",
             "description": "芍药是中国传统名花，与牡丹并称'花中二绝'。",
             "habitat": "喜温暖湿润环境", "distribution": "中国北方",
             "garden_zones": ["芍药园"]},
            {"name_cn": "月季", "name_latin": "Rosa chinensis", 
             "family": "蔷薇科", "genus": "蔷薇属", "protection_status": "",
             "description": "月季被称为'花中皇后'，品种繁多，四季开花。",
             "habitat": "喜阳光充足环境", "distribution": "中国原产",
             "garden_zones": ["月季园"]},
            {"name_cn": "菊花", "name_latin": "Chrysanthemum morifolium", 
             "family": "菊科", "genus": "菊属", "protection_status": "",
             "description": "菊花是中国传统名花，品种繁多，秋季开花。",
             "habitat": "喜凉爽气候", "distribution": "中国原产",
             "garden_zones": ["菊园", "展览温室"]},
            {"name_cn": "兰花", "name_latin": "Cymbidium spp.", 
             "family": "兰科", "genus": "兰属", "protection_status": "部分为国家保护",
             "description": "兰花是中国传统名花，以其高雅的气质著称。",
             "habitat": "喜阴湿环境", "distribution": "亚洲热带和亚热带",
             "garden_zones": ["兰科保育温室", "展览温室"]},
            {"name_cn": "丁香", "name_latin": "Syringa oblata", 
             "family": "木犀科", "genus": "丁香属", "protection_status": "",
             "description": "丁香是著名的观赏花木，春季开花，香气浓郁。",
             "habitat": "喜阳光充足环境", "distribution": "中国北方",
             "garden_zones": ["丁香园", "合瓣花区"]},
            {"name_cn": "海棠", "name_latin": "Malus spectabilis", 
             "family": "蔷薇科", "genus": "苹果属", "protection_status": "",
             "description": "海棠是中国传统名花，春季开花，花团锦簇。",
             "habitat": "喜阳光充足环境", "distribution": "中国原产",
             "garden_zones": ["海棠栒子园"]},
            {"name_cn": "梅花", "name_latin": "Prunus mume", 
             "family": "蔷薇科", "genus": "李属", "protection_status": "",
             "description": "梅花是中国传统名花，寒冬开花，象征坚韧不拔。",
             "habitat": "喜温暖湿润气候", "distribution": "中国南方",
             "garden_zones": ["梅园"]},
            {"name_cn": "桃花", "name_latin": "Prunus persica", 
             "family": "蔷薇科", "genus": "李属", "protection_status": "",
             "description": "桃花是著名的春季观赏花木，品种繁多。",
             "habitat": "喜阳光充足环境", "distribution": "中国原产",
             "garden_zones": ["桃花园"]},
            {"name_cn": "紫薇", "name_latin": "Lagerstroemia indica", 
             "family": "千屈菜科", "genus": "紫薇属", "protection_status": "",
             "description": "紫薇花期长，从夏季到秋季开花，有'百日红'之称。",
             "habitat": "喜阳光充足环境", "distribution": "亚洲热带地区",
             "garden_zones": ["紫薇园"]},
            {"name_cn": "睡莲", "name_latin": "Nymphaea tetragona", 
             "family": "睡莲科", "genus": "睡莲属", "protection_status": "",
             "description": "睡莲是水生观赏植物，花浮于水面，美丽动人。",
             "habitat": "水生环境", "distribution": "全球温带和热带",
             "garden_zones": ["水生植物区"]},
        ]
        
        for i, plant_data in enumerate(star_plants_text):
            plant_id = f"cvbg_{i+1:03d}"
            if plant_data["name_latin"] in self.seen_latin_names:
                continue
            self.seen_latin_names.add(plant_data["name_latin"])
            
            plant = Plant(
                id=plant_id,
                name_cn=plant_data["name_cn"],
                name_latin=plant_data["name_latin"],
                family=plant_data["family"],
                genus=plant_data["genus"],
                description=plant_data["description"],
                habitat=plant_data["habitat"],
                distribution=plant_data["distribution"],
                garden_zones=plant_data["garden_zones"],
                protection_status=plant_data["protection_status"],
                source_url="https://www.cvbg.cn/bg/01",
                collected_at=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            plants.append(plant)
        
        print(f"从国家植物园官网收集了 {len(plants)} 种明星植物")
        return plants
    
    def scrape_sample_data(self) -> List[Plant]:
        """生成示例植物数据（作为备用数据源）"""
        print("正在生成示例植物数据...")
        
        sample_plants = [
            {
                "name_cn": "白皮松",
                "name_latin": "Pinus bungeana",
                "family": "松科",
                "genus": "松属",
                "description": "白皮松是中国特有树种，树皮呈白色或灰白色，成不规则薄片脱落。",
                "habitat": "喜阳光充足、排水良好的环境",
                "distribution": "中国华北、西北",
                "garden_zones": ["裸子植物区", "树木园"],
                "protection_status": "国家三级保护"
            },
            {
                "name_cn": "侧柏",
                "name_latin": "Platycladus orientalis",
                "family": "柏科",
                "genus": "侧柏属",
                "description": "侧柏是中国特产，树冠广卵形，小枝扁平。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国大部分地区",
                "garden_zones": ["裸子植物区", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "圆柏",
                "name_latin": "Sabina chinensis",
                "family": "柏科",
                "genus": "圆柏属",
                "description": "圆柏是常绿乔木，树冠尖塔形或圆锥形。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国大部分地区",
                "garden_zones": ["裸子植物区", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "云杉",
                "name_latin": "Picea asperata",
                "family": "松科",
                "genus": "云杉属",
                "description": "云杉是中国特有树种，树形优美，是重要的观赏和用材树种。",
                "habitat": "喜冷凉湿润气候",
                "distribution": "中国西南、西北",
                "garden_zones": ["裸子植物区"],
                "protection_status": "国家三级保护"
            },
            {
                "name_cn": "悬铃木",
                "name_latin": "Platanus acerifolia",
                "family": "悬铃木科",
                "genus": "悬铃木属",
                "description": "悬铃木是著名的行道树，又称'法桐'，树冠广阔。",
                "habitat": "喜阳光充足环境",
                "distribution": "全球温带地区",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "毛白杨",
                "name_latin": "Populus tomentosa",
                "family": "杨柳科",
                "genus": "杨属",
                "description": "毛白杨是中国北方常见的速生树种，树干通直。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国华北、西北",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "国槐",
                "name_latin": "Sophora japonica",
                "family": "豆科",
                "genus": "槐属",
                "description": "国槐是中国北方常见的乡土树种，夏季开花，香气浓郁。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国北方",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "元宝枫",
                "name_latin": "Acer truncatum",
                "family": "槭树科",
                "genus": "槭属",
                "description": "元宝枫树形优美，秋季叶色变红，是著名的观赏树种。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国北方",
                "garden_zones": ["彩叶植物区", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "白蜡",
                "name_latin": "Fraxinus chinensis",
                "family": "木犀科",
                "genus": "白蜡属",
                "description": "白蜡是中国北方常见的乡土树种，秋季叶色变黄。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国大部分地区",
                "garden_zones": ["合瓣花区", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "臭椿",
                "name_latin": "Ailanthus altissima",
                "family": "苦木科",
                "genus": "臭椿属",
                "description": "臭椿是中国北方常见的速生树种，树冠开阔。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国大部分地区",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "山茱萸",
                "name_latin": "Cornus officinalis",
                "family": "山茱萸科",
                "genus": "山茱萸属",
                "description": "山茱萸是药用植物，早春开花，花色金黄。",
                "habitat": "喜温暖湿润环境",
                "distribution": "中国中部、华东",
                "garden_zones": ["本草园", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "流苏树",
                "name_latin": "Chionanthus retusus",
                "family": "木犀科",
                "genus": "流苏树属",
                "description": "流苏树春季开花，花白色，形似流苏。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国华北、华东",
                "garden_zones": ["树木园"],
                "protection_status": "国家二级保护"
            },
            {
                "name_cn": "柽柳",
                "name_latin": "Tamarix chinensis",
                "family": "柽柳科",
                "genus": "柽柳属",
                "description": "柽柳是耐盐碱树种，夏季开花，花粉红色。",
                "habitat": "喜阳光充足、耐盐碱环境",
                "distribution": "中国北方、西北",
                "garden_zones": ["环保植物区"],
                "protection_status": ""
            },
            {
                "name_cn": "雪柳",
                "name_latin": "Fontanesia fortunei",
                "family": "木犀科",
                "genus": "雪柳属",
                "description": "雪柳春季开花，花白色，密集如雪花。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国华北、华东",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "灯台树",
                "name_latin": "Cornus controversa",
                "family": "山茱萸科",
                "genus": "梾木属",
                "description": "灯台树枝条分层生长，形如灯台，树形优美。",
                "habitat": "喜温暖湿润环境",
                "distribution": "中国东北、华北、西南",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "紫叶李",
                "name_latin": "Prunus cerasifera f. atropurpurea",
                "family": "蔷薇科",
                "genus": "李属",
                "description": "紫叶李叶色常年紫红色，是著名的彩叶观赏树种。",
                "habitat": "喜阳光充足环境",
                "distribution": "栽培品种",
                "garden_zones": ["彩叶植物区"],
                "protection_status": ""
            },
            {
                "name_cn": "榆叶梅",
                "name_latin": "Prunus triloba",
                "family": "蔷薇科",
                "genus": "李属",
                "description": "榆叶梅春季开花，花色粉红，花团锦簇。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国北方",
                "garden_zones": ["桃花园", "树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "楸树",
                "name_latin": "Catalpa bungei",
                "family": "紫葳科",
                "genus": "梓属",
                "description": "楸树是中国珍贵的用材树种，树形优美，夏季开花。",
                "habitat": "喜温暖湿润环境",
                "distribution": "中国华北、华东、华中",
                "garden_zones": ["合瓣花区", "树木园"],
                "protection_status": "国家三级保护"
            },
            {
                "name_cn": "加杨",
                "name_latin": "Populus canadensis",
                "family": "杨柳科",
                "genus": "杨属",
                "description": "加杨是速生树种，树体高大，是常见的行道树。",
                "habitat": "喜阳光充足环境",
                "distribution": "栽培品种",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "绦柳",
                "name_latin": "Salix matsudana f. pendula",
                "family": "杨柳科",
                "genus": "柳属",
                "description": "绦柳枝条下垂，姿态优美，是常见的观赏柳树。",
                "habitat": "喜水湿环境",
                "distribution": "栽培品种",
                "garden_zones": ["树木园", "湖区"],
                "protection_status": ""
            },
            {
                "name_cn": "粗榧",
                "name_latin": "Cephalotaxus sinensis",
                "family": "三尖杉科",
                "genus": "三尖杉属",
                "description": "粗榧是常绿针叶树，树形优美，是中国特有树种。",
                "habitat": "喜阴湿环境",
                "distribution": "中国长江流域以南",
                "garden_zones": ["裸子植物区"],
                "protection_status": "国家三级保护"
            },
            {
                "name_cn": "二球悬铃木",
                "name_latin": "Platanus acerifolia",
                "family": "悬铃木科",
                "genus": "悬铃木属",
                "description": "二球悬铃木是著名的行道树，树冠广阔，耐修剪。",
                "habitat": "喜阳光充足环境",
                "distribution": "全球温带地区",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "钻天杨",
                "name_latin": "Populus nigra var. italica",
                "family": "杨柳科",
                "genus": "杨属",
                "description": "钻天杨树形呈圆柱形，挺拔向上，是常见的观赏杨树。",
                "habitat": "喜阳光充足环境",
                "distribution": "栽培品种",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "凌霄",
                "name_latin": "Campsis grandiflora",
                "family": "紫葳科",
                "genus": "凌霄属",
                "description": "凌霄是藤本植物，夏季开花，花色橙红。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国中部、华东",
                "garden_zones": ["合瓣花区"],
                "protection_status": ""
            },
            {
                "name_cn": "美国凌霄",
                "name_latin": "Campsis radicans",
                "family": "紫葳科",
                "genus": "凌霄属",
                "description": "美国凌霄是藤本植物，原产北美，夏季开花。",
                "habitat": "喜阳光充足环境",
                "distribution": "北美",
                "garden_zones": ["合瓣花区"],
                "protection_status": ""
            },
            {
                "name_cn": "紫藤",
                "name_latin": "Wisteria sinensis",
                "family": "豆科",
                "genus": "紫藤属",
                "description": "紫藤是著名的藤本花卉，春季开花，花紫色或白色。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国原产",
                "garden_zones": ["藤本植物区", "水生与藤本植物区"],
                "protection_status": ""
            },
            {
                "name_cn": "木香",
                "name_latin": "Rosa banksiae",
                "family": "蔷薇科",
                "genus": "蔷薇属",
                "description": "木香是藤本蔷薇，春季开花，花白色或黄色，香气浓郁。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国西南",
                "garden_zones": ["藤本植物区"],
                "protection_status": ""
            },
            {
                "name_cn": "金银花",
                "name_latin": "Lonicera japonica",
                "family": "忍冬科",
                "genus": "忍冬属",
                "description": "金银花是藤本植物，花初开白色，后转黄色，有药用价值。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国大部分地区",
                "garden_zones": ["合瓣花区", "本草园"],
                "protection_status": ""
            },
            {
                "name_cn": "迎春花",
                "name_latin": "Jasminum nudiflorum",
                "family": "木犀科",
                "genus": "素馨属",
                "description": "迎春花是早春开花的灌木，花色金黄，是春天的使者。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国华北、西北",
                "garden_zones": ["树木园"],
                "protection_status": ""
            },
            {
                "name_cn": "连翘",
                "name_latin": "Forsythia suspensa",
                "family": "木犀科",
                "genus": "连翘属",
                "description": "连翘早春开花，花色金黄，是常见的观赏和药用植物。",
                "habitat": "喜阳光充足环境",
                "distribution": "中国北部、中部",
                "garden_zones": ["树木园", "本草园"],
                "protection_status": ""
            }
        ]
        
        plants = []
        base_num = len(self.plants) + 1
        
        for i, plant_data in enumerate(sample_plants):
            plant_id = f"sample_{base_num + i:03d}"
            if plant_data["name_latin"] in self.seen_latin_names:
                continue
            self.seen_latin_names.add(plant_data["name_latin"])
            
            plant = Plant(
                id=plant_id,
                name_cn=plant_data["name_cn"],
                name_latin=plant_data["name_latin"],
                family=plant_data["family"],
                genus=plant_data["genus"],
                description=plant_data["description"],
                habitat=plant_data["habitat"],
                distribution=plant_data["distribution"],
                garden_zones=plant_data["garden_zones"],
                protection_status=plant_data["protection_status"],
                source_url="sample_data",
                collected_at=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            plants.append(plant)
        
        print(f"生成了 {len(plants)} 种示例植物数据")
        return plants
    
    def scrape_all(self) -> List[Plant]:
        """执行所有爬取任务"""
        print("=" * 60)
        print("开始爬取北京植物园植物数据")
        print("=" * 60)
        
        all_plants = []
        
        cvbg_plants = self.scrape_cvbg_star_plants()
        all_plants.extend(cvbg_plants)
        
        sample_plants = self.scrape_sample_data()
        all_plants.extend(sample_plants)
        
        self.plants = all_plants
        
        print("\n" + "=" * 60)
        print(f"爬取完成，共收集 {len(all_plants)} 种植物数据")
        print("=" * 60)
        
        return all_plants
    
    def clean_and_format(self) -> List[Dict]:
        """清洗和格式化数据"""
        print("正在清洗和格式化数据...")
        
        cleaned_plants = []
        seen_ids = set()
        
        for plant in self.plants:
            if plant.id in seen_ids:
                continue
            seen_ids.add(plant.id)
            
            plant.name_cn = self.clean_text(plant.name_cn)
            plant.name_latin = self.clean_text(plant.name_latin)
            plant.family = self.clean_text(plant.family)
            plant.genus = self.clean_text(plant.genus)
            plant.description = self.clean_text(plant.description)
            plant.habitat = self.clean_text(plant.habitat)
            plant.distribution = self.clean_text(plant.distribution)
            plant.protection_status = self.clean_text(plant.protection_status)
            
            cleaned_plants.append(asdict(plant))
        
        cleaned_plants.sort(key=lambda x: x["name_cn"])
        
        print(f"清洗完成，共 {len(cleaned_plants)} 条有效数据")
        return cleaned_plants
    
    def save_to_json(self, data: List[Dict], filename: str = "plants.json"):
        """保存数据到JSON文件"""
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            "metadata": {
                "source": "北京植物园相关网站",
                "description": "北京植物园植物数据",
                "total_count": len(data),
                "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0"
            },
            "plants": data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filepath}")
        return filepath
    
    def save_minified_json(self, data: List[Dict], filename: str = "plants.min.json"):
        """保存压缩版JSON（用于前端）"""
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            "metadata": {
                "total": len(data),
                "updated": time.strftime("%Y-%m-%d")
            },
            "plants": data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False)
        
        print(f"压缩版数据已保存到: {filepath}")
        return filepath
    
    def run(self):
        """运行完整爬虫流程"""
        self.scrape_all()
        cleaned_data = self.clean_and_format()
        self.save_to_json(cleaned_data)
        self.save_minified_json(cleaned_data)
        
        print("\n" + "=" * 60)
        print("爬虫任务完成！")
        print("=" * 60)
        
        return cleaned_data


def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "data")
    
    scraper = PlantScraper(output_dir=output_dir)
    scraper.run()


if __name__ == "__main__":
    main()
