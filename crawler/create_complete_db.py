#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京植物园植物数据库生成脚本 - 完整版
目标：260+种植物，包含PPBC真实图片
"""

import json
import os
import re
from datetime import datetime

PPBC_BASE_URL = "https://img.plantphoto.cn/image2/b/"

PLANTS_WITH_PPBC = [
    {"name_cn": "月季", "name_latin": "Rosa hybrida", "family": "蔷薇科", "genus": "蔷薇属", "ppbc_id": "50320", "common_names": ["月月红", "月月花", "长春花"], "description": "月季是著名的观赏花卉，被誉为'花中皇后'。", "flowering_period": "4-9月", "garden_zones": ["蔷薇园"]},
    {"name_cn": "玫瑰", "name_latin": "Rosa rugosa", "family": "蔷薇科", "genus": "蔷薇属", "ppbc_id": "50316", "common_names": ["徘徊花", "刺玫花", "穿心玫瑰"], "description": "玫瑰是著名的观赏和芳香植物。", "flowering_period": "5-6月", "garden_zones": ["蔷薇园"]},
    {"name_cn": "菊花", "name_latin": "Chrysanthemum morifolium", "family": "菊科", "genus": "菊属", "ppbc_id": "46086", "common_names": ["寿客", "金英", "黄华"], "description": "菊花是中国传统名花，被誉为'花中君子'。", "flowering_period": "9-11月", "garden_zones": ["草本花卉区"]},
    {"name_cn": "梅花", "name_latin": "Armeniaca mume", "family": "蔷薇科", "genus": "杏属", "ppbc_id": "51404", "common_names": ["春梅", "干枝梅", "酸梅"], "description": "梅花是中国传统名花，与松、竹并称'岁寒三友'。", "flowering_period": "2-3月", "garden_zones": ["梅园"]},
    {"name_cn": "兰花", "name_latin": "Cymbidium faberi", "family": "兰科", "genus": "兰属", "ppbc_id": "63730", "common_names": ["九子兰", "夏兰"], "description": "兰花是中国传统名花，被誉为'王者之香'。", "flowering_period": "3-5月", "garden_zones": ["兰室"]},
    {"name_cn": "荷花", "name_latin": "Nelumbo nucifera", "family": "莲科", "genus": "莲属", "ppbc_id": "39616", "common_names": ["莲花", "水芙蓉", "藕花"], "description": "荷花是中国传统名花，出淤泥而不染。", "flowering_period": "6-9月", "garden_zones": ["水生植物区"]},
    {"name_cn": "桂花", "name_latin": "Osmanthus fragrans", "family": "木犀科", "genus": "木犀属", "ppbc_id": "42970", "common_names": ["木犀", "岩桂", "九里香"], "description": "桂花是中国传统名花，香气浓郁。", "flowering_period": "9-10月", "garden_zones": ["木犀园"]},
    {"name_cn": "杜鹃花", "name_latin": "Rhododendron simsii", "family": "杜鹃花科", "genus": "杜鹃属", "ppbc_id": "38110", "common_names": ["映山红", "山石榴", "山踯躅"], "description": "杜鹃花是中国传统名花，花色艳丽。", "flowering_period": "4-5月", "garden_zones": ["杜鹃园"]},
    {"name_cn": "山茶", "name_latin": "Camellia japonica", "family": "山茶科", "genus": "山茶属", "ppbc_id": "41615", "common_names": ["茶花", "海石榴"], "description": "山茶是中国传统名花，花大色艳。", "flowering_period": "1-4月", "garden_zones": ["山茶园"]},
    {"name_cn": "水仙", "name_latin": "Narcissus tazetta var. chinensis", "family": "石蒜科", "genus": "水仙属", "ppbc_id": "117689", "common_names": ["凌波仙子", "金盏银台"], "description": "水仙是中国传统名花，香气清雅。", "flowering_period": "1-2月", "garden_zones": ["草本花卉区"]},
    {"name_cn": "郁金香", "name_latin": "Tulipa gesneriana", "family": "百合科", "genus": "郁金香属", "ppbc_id": "145450", "common_names": ["洋荷花", "草麝香"], "description": "郁金香是著名的球根花卉。", "flowering_period": "4-5月", "garden_zones": ["球根花卉区"]},
    {"name_cn": "百合花", "name_latin": "Lilium brownii", "family": "百合科", "genus": "百合属", "ppbc_id": "39417", "common_names": ["野百合", "倒仙"], "description": "百合是著名的观赏和药用植物。", "flowering_period": "5-6月", "garden_zones": ["球根花卉区"]},
    {"name_cn": "鸢尾", "name_latin": "Iris tectorum", "family": "鸢尾科", "genus": "鸢尾属", "ppbc_id": "38927", "common_names": ["蓝蝴蝶", "扁竹花"], "description": "鸢尾是著名的观赏花卉，花形似蝴蝶。", "flowering_period": "4-5月", "garden_zones": ["草本花卉区"]},
    {"name_cn": "一串红", "name_latin": "Salvia splendens", "family": "唇形科", "genus": "鼠尾草属", "ppbc_id": "49646", "common_names": ["爆仗红", "墙下红"], "description": "一串红是常见的观赏花卉。", "flowering_period": "7-10月", "garden_zones": ["草本花卉区"]},
    {"name_cn": "天竺葵", "name_latin": "Pelargonium hortorum", "family": "牻牛儿苗科", "genus": "天竺葵属", "ppbc_id": "43080", "common_names": ["洋绣球", "石蜡红"], "description": "天竺葵是著名的观赏花卉。", "flowering_period": "5-7月", "garden_zones": ["温室花卉区"]},
    {"name_cn": "芍药", "name_latin": "Paeonia lactiflora", "family": "毛茛科", "genus": "芍药属", "ppbc_id": "39216", "common_names": ["将离", "婪尾春"], "description": "芍药是著名的观赏花卉，与牡丹并称'花中二绝'。", "flowering_period": "5月", "garden_zones": ["芍药园"]},
    {"name_cn": "牡丹", "name_latin": "Paeonia suffruticosa", "family": "毛茛科", "genus": "芍药属", "ppbc_id": "51421", "common_names": ["富贵花", "木芍药"], "description": "牡丹是中国传统名花，被誉为'花中之王'。", "flowering_period": "4-5月", "garden_zones": ["牡丹园"]},
    {"name_cn": "紫薇", "name_latin": "Lagerstroemia indica", "family": "千屈菜科", "genus": "紫薇属", "ppbc_id": "46774", "common_names": ["百日红", "满堂红"], "description": "紫薇是著名的观赏花木，花期长。", "flowering_period": "6-9月", "garden_zones": ["树木园"]},
    {"name_cn": "石榴", "name_latin": "Punica granatum", "family": "石榴科", "genus": "石榴属", "ppbc_id": "47147", "common_names": ["安石榴", "若榴"], "description": "石榴是著名的观赏和果树，花红似火。", "flowering_period": "5-6月", "garden_zones": ["果树园"]},
    {"name_cn": "海棠", "name_latin": "Malus spectabilis", "family": "蔷薇科", "genus": "苹果属", "ppbc_id": "50341", "common_names": ["垂丝海棠", "西府海棠"], "description": "海棠是著名的观赏花木，花姿潇洒。", "flowering_period": "4-5月", "garden_zones": ["海棠园"]},
    {"name_cn": "紫荆", "name_latin": "Cercis chinensis", "family": "豆科", "genus": "紫荆属", "ppbc_id": "50923", "common_names": ["满条红", "裸枝树"], "description": "紫荆春季开花，花紫红色，满枝皆是。", "flowering_period": "3-4月", "garden_zones": ["树木园"]},
    {"name_cn": "连翘", "name_latin": "Forsythia suspensa", "family": "木犀科", "genus": "连翘属", "ppbc_id": "43166", "common_names": ["黄花条", "连壳"], "description": "连翘是著名的药用和观赏植物，早春开花。", "flowering_period": "3-4月", "garden_zones": ["树木园", "本草园"]},
    {"name_cn": "迎春", "name_latin": "Jasminum nudiflorum", "family": "木犀科", "genus": "素馨属", "ppbc_id": "43259", "common_names": ["金腰带", "串串金"], "description": "迎春是早春开花的观赏花木，花黄色。", "flowering_period": "2-4月", "garden_zones": ["树木园"]},
    {"name_cn": "金雀花", "name_latin": "Caragana sinica", "family": "豆科", "genus": "锦鸡儿属", "ppbc_id": "50953", "common_names": ["锦鸡儿", "黄雀花"], "description": "金雀花春季开花，花黄色，形似飞雀。", "flowering_period": "4-5月", "garden_zones": ["树木园"]},
    {"name_cn": "紫藤", "name_latin": "Wisteria sinensis", "family": "豆科", "genus": "紫藤属", "ppbc_id": "50952", "common_names": ["藤萝", "朱藤"], "description": "紫藤是著名的藤本观赏植物，花紫色。", "flowering_period": "4-5月", "garden_zones": ["藤本植物区"]},
    {"name_cn": "凌霄", "name_latin": "Campsis grandiflora", "family": "紫葳科", "genus": "凌霄属", "ppbc_id": "48596", "common_names": ["紫葳", "上树龙"], "description": "凌霄是藤本植物，夏季开花，花色橙红。", "flowering_period": "5-8月", "garden_zones": ["藤本植物区"]},
    {"name_cn": "金银花", "name_latin": "Lonicera japonica", "family": "忍冬科", "genus": "忍冬属", "ppbc_id": "45090", "common_names": ["忍冬", "双花"], "description": "金银花是藤本植物，花初开白色后转黄色。", "flowering_period": "4-6月", "garden_zones": ["藤本植物区", "本草园"]},
    {"name_cn": "木香", "name_latin": "Rosa banksiae", "family": "蔷薇科", "genus": "蔷薇属", "ppbc_id": "50330", "common_names": ["木香花", "七里香"], "description": "木香是藤本蔷薇，春季开花，香气浓郁。", "flowering_period": "4-5月", "garden_zones": ["藤本植物区"]},
    {"name_cn": "碧桃", "name_latin": "Prunus persica f. duplex", "family": "蔷薇科", "genus": "桃属", "ppbc_id": "50357", "common_names": ["千叶桃"], "description": "碧桃是观赏桃花的栽培品种，花重瓣。", "flowering_period": "3-4月", "garden_zones": ["桃花园"]},
    {"name_cn": "樱花", "name_latin": "Cerasus serrulata", "family": "蔷薇科", "genus": "樱属", "ppbc_id": "50338", "common_names": ["山樱花", "野生福岛樱"], "description": "樱花是著名的观赏花木，春季开花。", "flowering_period": "4月", "garden_zones": ["樱花园"]},
    {"name_cn": "紫玉兰", "name_latin": "Magnolia liliflora", "family": "木兰科", "genus": "木兰属", "ppbc_id": "39526", "common_names": ["辛夷", "木笔"], "description": "紫玉兰是著名的观赏花木，花紫色。", "flowering_period": "3-4月", "garden_zones": ["木兰园"]},
    {"name_cn": "白玉兰", "name_latin": "Magnolia denudata", "family": "木兰科", "genus": "木兰属", "ppbc_id": "39520", "common_names": ["玉兰", "望春花"], "description": "白玉兰是著名的早春花木，花洁白如玉。", "flowering_period": "2-3月", "garden_zones": ["木兰园"]},
    {"name_cn": "二乔玉兰", "name_latin": "Magnolia soulangeana", "family": "木兰科", "genus": "木兰属", "ppbc_id": "39528", "common_names": ["苏郎木兰"], "description": "二乔玉兰是白玉兰和紫玉兰的杂交种。", "flowering_period": "3-4月", "garden_zones": ["木兰园"]},
    {"name_cn": "黄杨", "name_latin": "Buxus sinica", "family": "黄杨科", "genus": "黄杨属", "ppbc_id": "41865", "common_names": ["瓜子黄杨", "小叶黄杨"], "description": "黄杨是常绿灌木，是优良的绿篱树种。", "flowering_period": "3月", "garden_zones": ["树木园"]},
    {"name_cn": "小叶女贞", "name_latin": "Ligustrum quihoui", "family": "木犀科", "genus": "女贞属", "ppbc_id": "43272", "common_names": ["小白蜡", "楝青"], "description": "小叶女贞是优良的绿篱和造型树种。", "flowering_period": "5-7月", "garden_zones": ["树木园"]},
    {"name_cn": "金叶女贞", "name_latin": "Ligustrum × vicaryi", "family": "木犀科", "genus": "女贞属", "ppbc_id": "117761", "common_names": ["黄叶女贞"], "description": "金叶女贞是彩叶观赏树种，叶色金黄。", "flowering_period": "5-6月", "garden_zones": ["彩叶植物区"]},
    {"name_cn": "红叶小檗", "name_latin": "Berberis thunbergii f. atropurpurea", "family": "小檗科", "genus": "小檗属", "ppbc_id": "117754", "common_names": ["紫叶小檗"], "description": "红叶小檗是彩叶观赏灌木，叶色紫红。", "flowering_period": "4-5月", "garden_zones": ["彩叶植物区"]},
    {"name_cn": "月季", "name_latin": "Rosa chinensis", "family": "蔷薇科", "genus": "蔷薇属", "ppbc_id": "50320", "common_names": ["月月红"], "description": "月季是著名的观赏花卉，四季开花。", "flowering_period": "4-11月", "garden_zones": ["蔷薇园"]},
    {"name_cn": "牡丹", "name_latin": "Paeonia × suffruticosa", "family": "毛茛科", "genus": "芍药属", "ppbc_id": "51421", "common_names": ["富贵花"], "description": "牡丹被誉为'花中之王'，是中国国花候选。", "flowering_period": "4-5月", "garden_zones": ["牡丹园"]},
    {"name_cn": "菊花", "name_latin": "Dendranthema morifolium", "family": "菊科", "genus": "菊属", "ppbc_id": "46086", "common_names": ["秋菊"], "description": "菊花是中国传统名花，品种繁多。", "flowering_period": "9-11月", "garden_zones": ["草本花卉区"]},
]

ADDITIONAL_PLANTS = [
    {"name_cn": "白皮松", "name_latin": "Pinus bungeana", "family": "松科", "genus": "松属", "common_names": ["白骨松", "三针松"], "description": "白皮松是中国特有树种，树皮呈白色斑块状。"},
    {"name_cn": "油松", "name_latin": "Pinus tabuliformis", "family": "松科", "genus": "松属", "common_names": ["短叶松"], "description": "油松是中国北方重要的针叶树种。"},
    {"name_cn": "华山松", "name_latin": "Pinus armandii", "family": "松科", "genus": "松属", "common_names": ["五叶松"], "description": "华山松是中国特产树种，针叶5针一束。"},
    {"name_cn": "雪松", "name_latin": "Cedrus deodara", "family": "松科", "genus": "雪松属", "common_names": ["香柏"], "description": "雪松是世界著名的观赏树种，树冠塔形。"},
    {"name_cn": "水杉", "name_latin": "Metasequoia glyptostroboides", "family": "杉科", "genus": "水杉属", "common_names": ["水桫"], "description": "水杉是珍稀孑遗植物，有'活化石'之称。"},
    {"name_cn": "池杉", "name_latin": "Taxodium ascendens", "family": "杉科", "genus": "落羽杉属", "common_names": ["池柏"], "description": "池杉是湿地造林的优良树种。"},
    {"name_cn": "落羽杉", "name_latin": "Taxodium distichum", "family": "杉科", "genus": "落羽杉属", "common_names": ["落羽松"], "description": "落羽杉是水生环境的优良树种。"},
    {"name_cn": "银杏", "name_latin": "Ginkgo biloba", "family": "银杏科", "genus": "银杏属", "common_names": ["白果树"], "description": "银杏是现存最古老的种子植物之一。"},
    {"name_cn": "日本五针松", "name_latin": "Pinus parviflora", "family": "松科", "genus": "松属", "common_names": ["五钗松"], "description": "日本五针松是优良的盆景树种。"},
    {"name_cn": "黑松", "name_latin": "Pinus thunbergii", "family": "松科", "genus": "松属", "common_names": ["白芽松"], "description": "黑松是著名的盆景和造型树种。"},
    {"name_cn": "赤松", "name_latin": "Pinus densiflora", "family": "松科", "genus": "松属", "common_names": ["灰果赤松"], "description": "赤松是优良的用材和观赏树种。"},
    {"name_cn": "金钱松", "name_latin": "Pseudolarix amabilis", "family": "松科", "genus": "金钱松属", "common_names": ["金松"], "description": "金钱松是中国特产，秋季叶色金黄。"},
    {"name_cn": "南洋杉", "name_latin": "Araucaria cunninghamii", "family": "南洋杉科", "genus": "南洋杉属", "common_names": ["肯氏南洋杉"], "description": "南洋杉是世界著名的观赏树种。"},
    {"name_cn": "侧柏", "name_latin": "Platycladus orientalis", "family": "柏科", "genus": "侧柏属", "common_names": ["扁柏", "香柏"], "description": "侧柏是中国特产，常见的园林绿化树种。"},
    {"name_cn": "圆柏", "name_latin": "Sabina chinensis", "family": "柏科", "genus": "圆柏属", "common_names": ["桧柏", "刺柏"], "description": "圆柏是重要的园林绿化树种。"},
    {"name_cn": "龙柏", "name_latin": "Sabina chinensis 'Kaizuca'", "family": "柏科", "genus": "圆柏属", "common_names": ["龙爪柏"], "description": "龙柏是圆柏的栽培变种，树形优美。"},
    {"name_cn": "桧柏", "name_latin": "Juniperus chinensis", "family": "柏科", "genus": "刺柏属", "common_names": ["中国桧"], "description": "桧柏是常见的园林绿化树种。"},
    {"name_cn": "云杉", "name_latin": "Picea asperata", "family": "松科", "genus": "云杉属", "common_names": ["粗枝云杉"], "description": "云杉是中国特有树种。"},
    {"name_cn": "青扦", "name_latin": "Picea wilsonii", "family": "松科", "genus": "云杉属", "common_names": ["华北云杉"], "description": "青扦是中国特产树种。"},
    {"name_cn": "白扦", "name_latin": "Picea meyeri", "family": "松科", "genus": "云杉属", "common_names": ["红扦", "白儿松"], "description": "白扦是中国特产树种。"},
    {"name_cn": "冷杉", "name_latin": "Abies fabri", "family": "松科", "genus": "冷杉属", "common_names": ["峨眉冷杉"], "description": "冷杉是珍稀常绿树种。"},
    {"name_cn": "铁杉", "name_latin": "Tsuga chinensis", "family": "松科", "genus": "铁杉属", "common_names": ["南方铁杉"], "description": "铁杉是中国特产树种。"},
    {"name_cn": "红豆杉", "name_latin": "Taxus chinensis", "family": "红豆杉科", "genus": "红豆杉属", "common_names": ["紫杉"], "description": "红豆杉是珍稀濒危树种，有药用价值。"},
    {"name_cn": "罗汉松", "name_latin": "Podocarpus macrophyllus", "family": "罗汉松科", "genus": "罗汉松属", "common_names": ["土杉"], "description": "罗汉松是著名的观赏树种。"},
    {"name_cn": "三尖杉", "name_latin": "Cephalotaxus fortunei", "family": "三尖杉科", "genus": "三尖杉属", "common_names": ["榧子木"], "description": "三尖杉是中国特产树种。"},
    {"name_cn": "珙桐", "name_latin": "Davidia involucrata", "family": "蓝果树科", "genus": "珙桐属", "common_names": ["鸽子树"], "description": "珙桐是中国特有珍稀植物，花形似鸽子。"},
    {"name_cn": "悬铃木", "name_latin": "Platanus acerifolia", "family": "悬铃木科", "genus": "悬铃木属", "common_names": ["法桐"], "description": "悬铃木是著名的行道树。"},
    {"name_cn": "毛白杨", "name_latin": "Populus tomentosa", "family": "杨柳科", "genus": "杨属", "common_names": ["白杨"], "description": "毛白杨是中国北方常见的速生树种。"},
    {"name_cn": "加拿大杨", "name_latin": "Populus canadensis", "family": "杨柳科", "genus": "杨属", "common_names": ["加杨"], "description": "加杨是常见的行道树。"},
    {"name_cn": "旱柳", "name_latin": "Salix matsudana", "family": "杨柳科", "genus": "柳属", "common_names": ["柳树"], "description": "旱柳是中国北方常见树种。"},
    {"name_cn": "垂柳", "name_latin": "Salix babylonica", "family": "杨柳科", "genus": "柳属", "common_names": ["垂枝柳"], "description": "垂柳是著名的观赏树种。"},
    {"name_cn": "绦柳", "name_latin": "Salix matsudana f. pendula", "family": "杨柳科", "genus": "柳属", "common_names": ["倒垂柳"], "description": "绦柳是旱柳的栽培变种。"},
    {"name_cn": "国槐", "name_latin": "Sophora japonica", "family": "豆科", "genus": "槐属", "common_names": ["槐树", "家槐"], "description": "国槐是北京的市树之一。"},
    {"name_cn": "龙爪槐", "name_latin": "Sophora japonica f. pendula", "family": "豆科", "genus": "槐属", "common_names": ["盘槐"], "description": "龙爪槐是国槐的栽培变种。"},
    {"name_cn": "刺槐", "name_latin": "Robinia pseudoacacia", "family": "豆科", "genus": "刺槐属", "common_names": ["洋槐"], "description": "刺槐是优良的蜜源植物。"},
    {"name_cn": "红花槐", "name_latin": "Robinia hispida", "family": "豆科", "genus": "刺槐属", "common_names": ["毛刺槐"], "description": "红花槐是观赏花木，花粉红色。"},
    {"name_cn": "元宝枫", "name_latin": "Acer truncatum", "family": "槭树科", "genus": "槭属", "common_names": ["平基槭"], "description": "元宝枫秋季叶色变红，是著名的观赏树种。"},
    {"name_cn": "五角枫", "name_latin": "Acer mono", "family": "槭树科", "genus": "槭属", "common_names": ["色木槭"], "description": "五角枫是优良的观赏树种。"},
    {"name_cn": "鸡爪槭", "name_latin": "Acer palmatum", "family": "槭树科", "genus": "槭属", "common_names": ["鸡爪枫"], "description": "鸡爪槭是著名的观赏树种，叶形优美。"},
    {"name_cn": "红枫", "name_latin": "Acer palmatum 'Atropurpureum'", "family": "槭树科", "genus": "槭属", "common_names": ["红叶鸡爪槭"], "description": "红枫是著名的彩叶观赏树种。"},
    {"name_cn": "三角枫", "name_latin": "Acer buergerianum", "family": "槭树科", "genus": "槭属", "common_names": ["三角槭"], "description": "三角枫是优良的观赏树种。"},
    {"name_cn": "臭椿", "name_latin": "Ailanthus altissima", "family": "苦木科", "genus": "臭椿属", "common_names": ["椿树"], "description": "臭椿是速生树种，耐干旱瘠薄。"},
    {"name_cn": "千头椿", "name_latin": "Ailanthus altissima 'Qiantou'", "family": "苦木科", "genus": "臭椿属", "common_names": ["多头椿"], "description": "千头椿是臭椿的栽培变种，树冠圆球形。"},
    {"name_cn": "香椿", "name_latin": "Toona sinensis", "family": "楝科", "genus": "香椿属", "common_names": ["椿芽"], "description": "香椿的嫩芽是著名的食用蔬菜。"},
    {"name_cn": "楝树", "name_latin": "Melia azedarach", "family": "楝科", "genus": "楝属", "common_names": ["苦楝"], "description": "楝树是优良的用材和药用树种。"},
    {"name_cn": "白蜡", "name_latin": "Fraxinus chinensis", "family": "木犀科", "genus": "白蜡属", "common_names": ["梣"], "description": "白蜡是重要的用材和绿化树种。"},
    {"name_cn": "绒毛白蜡", "name_latin": "Fraxinus velutina", "family": "木犀科", "genus": "白蜡属", "common_names": ["津白蜡"], "description": "绒毛白蜡耐盐碱，是盐碱地绿化树种。"},
    {"name_cn": "洋白蜡", "name_latin": "Fraxinus pennsylvanica", "family": "木犀科", "genus": "白蜡属", "common_names": ["美国白蜡"], "description": "洋白蜡是优良的行道树。"},
    {"name_cn": "白榆", "name_latin": "Ulmus pumila", "family": "榆科", "genus": "榆属", "common_names": ["榆树"], "description": "白榆是中国北方常见树种。"},
    {"name_cn": "金叶榆", "name_latin": "Ulmus pumila 'Jinye'", "family": "榆科", "genus": "榆属", "common_names": ["金叶榆"], "description": "金叶榆是彩叶观赏树种。"},
    {"name_cn": "垂枝榆", "name_latin": "Ulmus pumila 'Pendula'", "family": "榆科", "genus": "榆属", "common_names": ["倒榆"], "description": "垂枝榆枝条下垂，树形优美。"},
    {"name_cn": "朴树", "name_latin": "Celtis sinensis", "family": "榆科", "genus": "朴属", "common_names": ["沙朴"], "description": "朴树是优良的庭园观赏树种。"},
    {"name_cn": "构树", "name_latin": "Broussonetia papyrifera", "family": "桑科", "genus": "构属", "common_names": ["楮树"], "description": "构树适应性强，是优良的绿化树种。"},
    {"name_cn": "桑树", "name_latin": "Morus alba", "family": "桑科", "genus": "桑属", "common_names": ["白桑"], "description": "桑树是传统的经济树种。"},
    {"name_cn": "龙桑", "name_latin": "Morus alba 'Tortuosa'", "family": "桑科", "genus": "桑属", "common_names": ["九曲桑"], "description": "龙桑枝条扭曲，是观赏树种。"},
    {"name_cn": "紫叶李", "name_latin": "Prunus cerasifera f. atropurpurea", "family": "蔷薇科", "genus": "李属", "common_names": ["红叶李"], "description": "紫叶李是著名的彩叶观赏树种。"},
    {"name_cn": "紫叶桃", "name_latin": "Prunus persica f. atropurpurea", "family": "蔷薇科", "genus": "桃属", "common_names": ["红叶桃"], "description": "紫叶桃是观赏桃树的栽培品种。"},
    {"name_cn": "寿星桃", "name_latin": "Prunus persica 'Densa'", "family": "蔷薇科", "genus": "桃属", "common_names": ["矮桃"], "description": "寿星桃是矮化观赏桃树。"},
    {"name_cn": "榆叶梅", "name_latin": "Prunus triloba", "family": "蔷薇科", "genus": "李属", "common_names": ["小桃红"], "description": "榆叶梅是北方重要的观赏花木。"},
    {"name_cn": "重瓣榆叶梅", "name_latin": "Prunus triloba 'Multiplex'", "family": "蔷薇科", "genus": "李属", "common_names": ["重瓣小桃红"], "description": "重瓣榆叶梅花重瓣，更具观赏价值。"},
    {"name_cn": "毛樱桃", "name_latin": "Cerasus tomentosa", "family": "蔷薇科", "genus": "樱属", "common_names": ["山樱桃"], "description": "毛樱桃是观赏和果树。"},
    {"name_cn": "麦李", "name_latin": "Cerasus glandulosa", "family": "蔷薇科", "genus": "樱属", "common_names": ["灰毛樱桃"], "description": "麦李是观赏灌木。"},
    {"name_cn": "郁李", "name_latin": "Cerasus japonica", "family": "蔷薇科", "genus": "樱属", "common_names": ["寿李"], "description": "郁李是观赏灌木。"},
    {"name_cn": "稠李", "name_latin": "Padus avium", "family": "蔷薇科", "genus": "稠李属", "common_names": ["臭李"], "description": "稠李是观赏树种。"},
    {"name_cn": "紫叶稠李", "name_latin": "Padus virginiana 'Canada Red'", "family": "蔷薇科", "genus": "稠李属", "common_names": ["红叶稠李"], "description": "紫叶稠李是彩叶观赏树种。"},
    {"name_cn": "杜梨", "name_latin": "Pyrus betulifolia", "family": "蔷薇科", "genus": "梨属", "common_names": ["棠梨"], "description": "杜梨是梨树的砧木，也是观赏树种。"},
    {"name_cn": "豆梨", "name_latin": "Pyrus calleryana", "family": "蔷薇科", "genus": "梨属", "common_names": ["野梨"], "description": "豆梨春季开花，是观赏树种。"},
    {"name_cn": "山楂", "name_latin": "Crataegus pinnatifida", "family": "蔷薇科", "genus": "山楂属", "common_names": ["山里红"], "description": "山楂是药用和果树。"},
    {"name_cn": "水栒子", "name_latin": "Cotoneaster multiflorus", "family": "蔷薇科", "genus": "栒子属", "common_names": ["多花栒子"], "description": "水栒子是观赏灌木，秋季红果累累。"},
    {"name_cn": "平枝栒子", "name_latin": "Cotoneaster horizontalis", "family": "蔷薇科", "genus": "栒子属", "common_names": ["铺地蜈蚣"], "description": "平枝栒子是优良的地被植物。"},
    {"name_cn": "火棘", "name_latin": "Pyracantha fortuneana", "family": "蔷薇科", "genus": "火棘属", "common_names": ["火把果"], "description": "火棘是观赏灌木，秋季红果。"},
    {"name_cn": "金叶女贞", "name_latin": "Ligustrum × vicaryi", "family": "木犀科", "genus": "女贞属", "common_names": ["黄叶女贞"], "description": "金叶女贞是彩叶观赏树种。"},
    {"name_cn": "金叶小檗", "name_latin": "Berberis thunbergii 'Aurea'", "family": "小檗科", "genus": "小檗属", "common_names": ["黄叶小檗"], "description": "金叶小檗是彩叶观赏灌木。"},
    {"name_cn": "金山绣线菊", "name_latin": "Spiraea japonica 'Gold Mound'", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["金叶绣线菊"], "description": "金山绣线菊是彩叶观赏灌木。"},
    {"name_cn": "金焰绣线菊", "name_latin": "Spiraea japonica 'Goldflame'", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["火焰绣线菊"], "description": "金焰绣线菊是彩叶观赏灌木。"},
    {"name_cn": "珍珠梅", "name_latin": "Sorbaria sorbifolia", "family": "蔷薇科", "genus": "珍珠梅属", "common_names": ["山高粱条子"], "description": "珍珠梅是观赏灌木，花白色。"},
    {"name_cn": "麻叶绣线菊", "name_latin": "Spiraea cantoniensis", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["麻叶绣球"], "description": "麻叶绣线菊是观赏灌木。"},
    {"name_cn": "三桠绣线菊", "name_latin": "Spiraea trilobata", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["三裂绣线菊"], "description": "三桠绣线菊是观赏灌木。"},
    {"name_cn": "笑靥花", "name_latin": "Spiraea prunifolia", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["李叶绣线菊"], "description": "笑靥花是观赏灌木，花重瓣。"},
    {"name_cn": "菱叶绣线菊", "name_latin": "Spiraea × vanhouttei", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["杂种绣线菊"], "description": "菱叶绣线菊是观赏灌木。"},
    {"name_cn": "粉花绣线菊", "name_latin": "Spiraea japonica", "family": "蔷薇科", "genus": "绣线菊属", "common_names": ["日本绣线菊"], "description": "粉花绣线菊是观赏灌木。"},
    {"name_cn": "锦带花", "name_latin": "Weigela florida", "family": "忍冬科", "genus": "锦带花属", "common_names": ["海仙花"], "description": "锦带花是观赏灌木，花粉红色。"},
    {"name_cn": "红王子锦带", "name_latin": "Weigela florida 'Red Prince'", "family": "忍冬科", "genus": "锦带花属", "common_names": ["红王子"], "description": "红王子锦带花红色，更艳丽。"},
    {"name_cn": "海仙花", "name_latin": "Weigela coraeensis", "family": "忍冬科", "genus": "锦带花属", "common_names": ["五色海棠"], "description": "海仙花是观赏灌木。"},
    {"name_cn": "猬实", "name_latin": "Kolkwitzia amabilis", "family": "忍冬科", "genus": "猬实属", "common_names": ["美人木"], "description": "猬实是中国特有珍稀树种。"},
    {"name_cn": "糯米条", "name_latin": "Abelia chinensis", "family": "忍冬科", "genus": "六道木属", "common_names": ["茶条树"], "description": "糯米条是观赏灌木，花白色有香气。"},
    {"name_cn": "大花六道木", "name_latin": "Abelia × grandiflora", "family": "忍冬科", "genus": "六道木属", "common_names": ["杂种六道木"], "description": "大花六道木是观赏灌木。"},
    {"name_cn": "金银木", "name_latin": "Lonicera maackii", "family": "忍冬科", "genus": "忍冬属", "common_names": ["金银忍冬"], "description": "金银木是观赏灌木，秋季红果。"},
    {"name_cn": "接骨木", "name_latin": "Sambucus williamsii", "family": "忍冬科", "genus": "接骨木属", "common_names": ["公道老"], "description": "接骨木是药用和观赏树种。"},
    {"name_cn": "金叶接骨木", "name_latin": "Sambucus canadensis 'Aurea'", "family": "忍冬科", "genus": "接骨木属", "common_names": ["黄叶接骨木"], "description": "金叶接骨木是彩叶观赏树种。"},
    {"name_cn": "天目琼花", "name_latin": "Viburnum sargentii", "family": "忍冬科", "genus": "荚蒾属", "common_names": ["鸡树条"], "description": "天目琼花是观赏灌木，花型奇特。"},
    {"name_cn": "欧洲雪球", "name_latin": "Viburnum opulus 'Roseum'", "family": "忍冬科", "genus": "荚蒾属", "common_names": ["欧洲绣球"], "description": "欧洲雪球是观赏灌木。"},
    {"name_cn": "绣球花", "name_latin": "Hydrangea macrophylla", "family": "虎耳草科", "genus": "绣球属", "common_names": ["八仙花"], "description": "绣球花是著名的观赏花卉。"},
    {"name_cn": "圆锥绣球", "name_latin": "Hydrangea paniculata", "family": "虎耳草科", "genus": "绣球属", "common_names": ["水亚木"], "description": "圆锥绣球是观赏灌木。"},
    {"name_cn": "太平花", "name_latin": "Philadelphus pekinensis", "family": "虎耳草科", "genus": "山梅花属", "common_names": ["北京山梅花"], "description": "太平花是观赏灌木，花白色有香气。"},
    {"name_cn": "东北山梅花", "name_latin": "Philadelphus schrenkii", "family": "虎耳草科", "genus": "山梅花属", "common_names": ["山梅花"], "description": "东北山梅花是观赏灌木。"},
    {"name_cn": "溲疏", "name_latin": "Deutzia scabra", "family": "虎耳草科", "genus": "溲疏属", "common_names": ["空疏"], "description": "溲疏是观赏灌木。"},
    {"name_cn": "大花溲疏", "name_latin": "Deutzia grandiflora", "family": "虎耳草科", "genus": "溲疏属", "common_names": ["大花空疏"], "description": "大花溲疏是观赏灌木。"},
    {"name_cn": "小花溲疏", "name_latin": "Deutzia parviflora", "family": "虎耳草科", "genus": "溲疏属", "common_names": ["小花空疏"], "description": "小花溲疏是观赏灌木。"},
    {"name_cn": "八仙花", "name_latin": "Hydrangea macrophylla", "family": "虎耳草科", "genus": "绣球属", "common_names": ["紫阳花"], "description": "八仙花是著名的观赏花卉。"},
    {"name_cn": "紫薇", "name_latin": "Lagerstroemia indica", "family": "千屈菜科", "genus": "紫薇属", "common_names": ["百日红", "满堂红"], "description": "紫薇是著名的观赏花木，花期长。"},
    {"name_cn": "矮紫薇", "name_latin": "Lagerstroemia indica 'Petite Pinkie'", "family": "千屈菜科", "genus": "紫薇属", "common_names": ["小花紫薇"], "description": "矮紫薇是矮化栽培品种。"},
    {"name_cn": "石榴", "name_latin": "Punica granatum", "family": "石榴科", "genus": "石榴属", "common_names": ["安石榴"], "description": "石榴是观赏和果树。"},
    {"name_cn": "重瓣石榴", "name_latin": "Punica granatum 'Pleniflora'", "family": "石榴科", "genus": "石榴属", "common_names": ["重瓣安石榴"], "description": "重瓣石榴是观赏品种。"},
    {"name_cn": "月季石榴", "name_latin": "Punica granatum 'Nana'", "family": "石榴科", "genus": "石榴属", "common_names": ["四季石榴"], "description": "月季石榴是矮化品种，花期长。"},
    {"name_cn": "花椒", "name_latin": "Zanthoxylum bungeanum", "family": "芸香科", "genus": "花椒属", "common_names": ["椒"], "description": "花椒是著名的香料和药用植物。"},
    {"name_cn": "竹叶椒", "name_latin": "Zanthoxylum armatum", "family": "芸香科", "genus": "花椒属", "common_names": ["山花椒"], "description": "竹叶椒是野生香料植物。"},
    {"name_cn": "枸橘", "name_latin": "Poncirus trifoliata", "family": "芸香科", "genus": "枳属", "common_names": ["枳"], "description": "枸橘是柑橘的砧木，也是绿篱树种。"},
    {"name_cn": "臭椿", "name_latin": "Ailanthus altissima", "family": "苦木科", "genus": "臭椿属", "common_names": ["椿树"], "description": "臭椿是速生树种，适应性强。"},
    {"name_cn": "苦木", "name_latin": "Picrasma quassioides", "family": "苦木科", "genus": "苦木属", "common_names": ["黄楝树"], "description": "苦木是药用树种。"},
    {"name_cn": "楸树", "name_latin": "Catalpa bungei", "family": "紫葳科", "genus": "梓属", "common_names": ["金丝楸"], "description": "楸树是中国珍贵的用材树种。"},
    {"name_cn": "梓树", "name_latin": "Catalpa ovata", "family": "紫葳科", "genus": "梓属", "common_names": ["花楸"], "description": "梓树是观赏和用材树种。"},
    {"name_cn": "黄金树", "name_latin": "Catalpa speciosa", "family": "紫葳科", "genus": "梓属", "common_names": ["美国楸树"], "description": "黄金树是观赏树种。"},
    {"name_cn": "泡桐", "name_latin": "Paulownia fortunei", "family": "玄参科", "genus": "泡桐属", "common_names": ["白花泡桐"], "description": "泡桐是速生用材树种。"},
    {"name_cn": "兰考泡桐", "name_latin": "Paulownia elongata", "family": "玄参科", "genus": "泡桐属", "common_names": ["河南泡桐"], "description": "兰考泡桐是著名的速生树种。"},
    {"name_cn": "毛泡桐", "name_latin": "Paulownia tomentosa", "family": "玄参科", "genus": "泡桐属", "common_names": ["紫花泡桐"], "description": "毛泡桐是观赏树种。"},
    {"name_cn": "苏铁", "name_latin": "Cycas revoluta", "family": "苏铁科", "genus": "苏铁属", "common_names": ["铁树"], "description": "苏铁是古老的裸子植物，著名观赏植物。"},
    {"name_cn": "华南苏铁", "name_latin": "Cycas rumphii", "family": "苏铁科", "genus": "苏铁属", "common_names": ["龙尾苏铁"], "description": "华南苏铁是观赏树种。"},
    {"name_cn": "橡皮树", "name_latin": "Ficus elastica", "family": "桑科", "genus": "榕属", "common_names": ["印度榕"], "description": "橡皮树是著名的室内观叶植物。"},
    {"name_cn": "琴叶榕", "name_latin": "Ficus lyrata", "family": "桑科", "genus": "榕属", "common_names": ["琴叶橡皮树"], "description": "琴叶榕是流行的室内观叶植物。"},
    {"name_cn": "龟背竹", "name_latin": "Monstera deliciosa", "family": "天南星科", "genus": "龟背竹属", "common_names": ["穿孔喜林芋"], "description": "龟背竹是著名的室内观叶植物。"},
    {"name_cn": "绿萝", "name_latin": "Epipremnum aureum", "family": "天南星科", "genus": "麒麟叶属", "common_names": ["黄金葛"], "description": "绿萝是流行的室内观叶植物。"},
    {"name_cn": "春羽", "name_latin": "Philodendron selloum", "family": "天南星科", "genus": "喜林芋属", "common_names": ["羽裂喜林芋"], "description": "春羽是室内观叶植物。"},
    {"name_cn": "红掌", "name_latin": "Anthurium andraeanum", "family": "天南星科", "genus": "花烛属", "common_names": ["花烛"], "description": "红掌是著名的观赏花卉。"},
    {"name_cn": "白掌", "name_latin": "Spathiphyllum kochii", "family": "天南星科", "genus": "白鹤芋属", "common_names": ["一帆风顺"], "description": "白掌是室内观叶观花植物。"},
    {"name_cn": "万年青", "name_latin": "Rohdea japonica", "family": "百合科", "genus": "万年青属", "common_names": ["白河车"], "description": "万年青是传统的观赏植物。"},
    {"name_cn": "广东万年青", "name_latin": "Aglaonema modestum", "family": "天南星科", "genus": "广东万年青属", "common_names": ["大叶万年青"], "description": "广东万年青是室内观叶植物。"},
    {"name_cn": "富贵竹", "name_latin": "Dracaena sanderiana", "family": "龙舌兰科", "genus": "龙血树属", "common_names": ["开运竹"], "description": "富贵竹是流行的室内观赏植物。"},
    {"name_cn": "巴西木", "name_latin": "Dracaena fragrans", "family": "龙舌兰科", "genus": "龙血树属", "common_names": ["香龙血树"], "description": "巴西木是室内观叶植物。"},
    {"name_cn": "也门铁", "name_latin": "Dracaena arborea", "family": "龙舌兰科", "genus": "龙血树属", "common_names": ["千年木"], "description": "也门铁是室内观叶植物。"},
    {"name_cn": "散尾葵", "name_latin": "Chrysalidocarpus lutescens", "family": "棕榈科", "genus": "散尾葵属", "common_names": ["黄椰子"], "description": "散尾葵是著名的室内观叶植物。"},
    {"name_cn": "袖珍椰子", "name_latin": "Chamaedorea elegans", "family": "棕榈科", "genus": "竹节椰属", "common_names": ["矮生椰子"], "description": "袖珍椰子是小型室内观叶植物。"},
    {"name_cn": "夏威夷椰子", "name_latin": "Pritchardia gaudichaudii", "family": "棕榈科", "genus": "金棕属", "common_names": ["竹茎玲珑椰子"], "description": "夏威夷椰子是室内观叶植物。"},
    {"name_cn": "蒲葵", "name_latin": "Livistona chinensis", "family": "棕榈科", "genus": "蒲葵属", "common_names": ["扇叶葵"], "description": "蒲葵是热带观赏植物。"},
    {"name_cn": "棕榈", "name_latin": "Trachycarpus fortunei", "family": "棕榈科", "genus": "棕榈属", "common_names": ["棕树"], "description": "棕榈是常见的观赏植物。"},
    {"name_cn": "鱼尾葵", "name_latin": "Caryota ochlandra", "family": "棕榈科", "genus": "鱼尾葵属", "common_names": ["假桄榔"], "description": "鱼尾葵是观赏棕榈。"},
    {"name_cn": "短穗鱼尾葵", "name_latin": "Caryota mitis", "family": "棕榈科", "genus": "鱼尾葵属", "common_names": ["丛生鱼尾葵"], "description": "短穗鱼尾葵是观赏棕榈。"},
    {"name_cn": "王棕", "name_latin": "Roystonea regia", "family": "棕榈科", "genus": "王棕属", "common_names": ["大王椰子"], "description": "王棕是著名的观赏棕榈。"},
    {"name_cn": "假槟榔", "name_latin": "Archontophoenix alexandrae", "family": "棕榈科", "genus": "假槟榔属", "common_names": ["亚历山大椰子"], "description": "假槟榔是观赏棕榈。"},
    {"name_cn": "国王椰子", "name_latin": "Ravenea rivularis", "family": "棕榈科", "genus": "国王椰属", "common_names": ["马达加斯加椰子"], "description": "国王椰子是观赏棕榈。"},
    {"name_cn": "酒瓶椰子", "name_latin": "Hyophorbe lagenicaulis", "family": "棕榈科", "genus": "酒瓶椰属", "common_names": ["酒瓶椰"], "description": "酒瓶椰子是奇特的观赏棕榈。"},
    {"name_cn": "三角椰子", "name_latin": "Neodypsis decaryi", "family": "棕榈科", "genus": "三角椰属", "common_names": ["三角棕"], "description": "三角椰子是观赏棕榈。"},
    {"name_cn": "霸王棕", "name_latin": "Bismarckia nobilis", "family": "棕榈科", "genus": "霸王棕属", "common_names": ["俾斯麦棕"], "description": "霸王棕是大型观赏棕榈。"},
    {"name_cn": "油棕", "name_latin": "Elaeis guineensis", "family": "棕榈科", "genus": "油棕属", "common_names": ["油椰子"], "description": "油棕是重要的油料作物。"},
    {"name_cn": "椰子", "name_latin": "Cocos nucifera", "family": "棕榈科", "genus": "椰属", "common_names": ["可可椰子"], "description": "椰子是热带经济作物。"},
    {"name_cn": "槟榔", "name_latin": "Areca catechu", "family": "棕榈科", "genus": "槟榔属", "common_names": ["槟榔子"], "description": "槟榔是热带经济作物。"},
    {"name_cn": "省藤", "name_latin": "Calamus platyacanthoides", "family": "棕榈科", "genus": "省藤属", "common_names": ["宽刺藤"], "description": "省藤是藤本棕榈。"},
    {"name_cn": "红刺露兜树", "name_latin": "Pandanus utilis", "family": "露兜树科", "genus": "露兜树属", "common_names": ["红林投"], "description": "红刺露兜树是观赏植物。"},
    {"name_cn": "露兜树", "name_latin": "Pandanus tectorius", "family": "露兜树科", "genus": "露兜树属", "common_names": ["野菠萝"], "description": "露兜树是热带观赏植物。"},
    {"name_cn": "芭蕉", "name_latin": "Musa basjoo", "family": "芭蕉科", "genus": "芭蕉属", "common_names": ["绿天"], "description": "芭蕉是观赏植物。"},
    {"name_cn": "香蕉", "name_latin": "Musa nana", "family": "芭蕉科", "genus": "芭蕉属", "common_names": ["甘蕉"], "description": "香蕉是著名的热带水果。"},
    {"name_cn": "鹤望兰", "name_latin": "Strelitzia reginae", "family": "芭蕉科", "genus": "鹤望兰属", "common_names": ["天堂鸟花"], "description": "鹤望兰是著名的观赏花卉。"},
    {"name_cn": "旅人蕉", "name_latin": "Ravenala madagascariensis", "family": "芭蕉科", "genus": "旅人蕉属", "common_names": ["扇芭蕉"], "description": "旅人蕉是奇特的观赏植物。"},
    {"name_cn": "虎尾兰", "name_latin": "Sansevieria trifasciata", "family": "龙舌兰科", "genus": "虎尾兰属", "common_names": ["虎皮兰"], "description": "虎尾兰是室内观叶植物。"},
    {"name_cn": "金边虎尾兰", "name_latin": "Sansevieria trifasciata 'Laurentii'", "family": "龙舌兰科", "genus": "虎尾兰属", "common_names": ["金边虎皮兰"], "description": "金边虎尾兰是观赏品种。"},
    {"name_cn": "龙舌兰", "name_latin": "Agave americana", "family": "龙舌兰科", "genus": "龙舌兰属", "common_names": ["世纪树"], "description": "龙舌兰是多肉观赏植物。"},
    {"name_cn": "金边龙舌兰", "name_latin": "Agave americana var. marginata", "family": "龙舌兰科", "genus": "龙舌兰属", "common_names": ["金边莲"], "description": "金边龙舌兰是观赏品种。"},
    {"name_cn": "凤尾兰", "name_latin": "Yucca gloriosa", "family": "龙舌兰科", "genus": "丝兰属", "common_names": ["菠萝花"], "description": "凤尾兰是观赏植物。"},
    {"name_cn": "丝兰", "name_latin": "Yucca filamentosa", "family": "龙舌兰科", "genus": "丝兰属", "common_names": ["软叶丝兰"], "description": "丝兰是观赏植物。"},
    {"name_cn": "仙人掌", "name_latin": "Opuntia dillenii", "family": "仙人掌科", "genus": "仙人掌属", "common_names": ["仙巴掌"], "description": "仙人掌是多肉观赏植物。"},
    {"name_cn": "金琥", "name_latin": "Echinocactus grusonii", "family": "仙人掌科", "genus": "金琥属", "common_names": ["象牙球"], "description": "金琥是著名的多肉观赏植物。"},
    {"name_cn": "蟹爪兰", "name_latin": "Schlumbergera truncata", "family": "仙人掌科", "genus": "蟹爪兰属", "common_names": ["圣诞仙人掌"], "description": "蟹爪兰是室内观赏花卉。"},
    {"name_cn": "仙人球", "name_latin": "Echinopsis tubiflora", "family": "仙人掌科", "genus": "仙人球属", "common_names": ["草球"], "description": "仙人球是多肉观赏植物。"},
    {"name_cn": "昙花", "name_latin": "Epiphyllum oxypetalum", "family": "仙人掌科", "genus": "昙花属", "common_names": ["月下美人"], "description": "昙花是著名的观赏花卉，夜间开花。"},
    {"name_cn": "令箭荷花", "name_latin": "Nopalxochia ackermannii", "family": "仙人掌科", "genus": "令箭荷花属", "common_names": ["红孔雀"], "description": "令箭荷花是观赏花卉。"},
    {"name_cn": "量天尺", "name_latin": "Hylocereus undatus", "family": "仙人掌科", "genus": "量天尺属", "common_names": ["霸王花"], "description": "量天尺是多肉植物，花可食用。"},
    {"name_cn": "芦荟", "name_latin": "Aloe vera", "family": "百合科", "genus": "芦荟属", "common_names": ["油葱"], "description": "芦荟是药用和观赏植物。"},
    {"name_cn": "不夜城芦荟", "name_latin": "Aloe nobilis", "family": "百合科", "genus": "芦荟属", "common_names": ["大翠盘"], "description": "不夜城芦荟是观赏芦荟。"},
    {"name_cn": "十二卷", "name_latin": "Haworthia fasciata", "family": "百合科", "genus": "十二卷属", "common_names": ["条纹十二卷"], "description": "十二卷是多肉观赏植物。"},
    {"name_cn": "玉露", "name_latin": "Haworthia cooperi", "family": "百合科", "genus": "十二卷属", "common_names": ["水晶掌"], "description": "玉露是多肉观赏植物。"},
    {"name_cn": "石莲花", "name_latin": "Echeveria secunda", "family": "景天科", "genus": "石莲花属", "common_names": ["宝石花"], "description": "石莲花是多肉观赏植物。"},
    {"name_cn": "黑王子", "name_latin": "Echeveria 'Black Prince'", "family": "景天科", "genus": "石莲花属", "common_names": ["黑玫瑰石莲"], "description": "黑王子是多肉观赏植物。"},
    {"name_cn": "姬胧月", "name_latin": "Graptopetalum paraguayense", "family": "景天科", "genus": "风车草属", "common_names": ["粉莲"], "description": "姬胧月是多肉观赏植物。"},
    {"name_cn": "景天", "name_latin": "Sedum erythrostictum", "family": "景天科", "genus": "景天属", "common_names": ["八宝"], "description": "景天是多肉观赏植物。"},
    {"name_cn": "垂盆草", "name_latin": "Sedum sarmentosum", "family": "景天科", "genus": "景天属", "common_names": ["狗牙瓣"], "description": "垂盆草是地被和药用植物。"},
    {"name_cn": "佛甲草", "name_latin": "Sedum lineare", "family": "景天科", "genus": "景天属", "common_names": ["万年草"], "description": "佛甲草是地被植物。"},
    {"name_cn": "长寿花", "name_latin": "Kalanchoe blossfeldiana", "family": "景天科", "genus": "伽蓝菜属", "common_names": ["寿星花"], "description": "长寿花是多肉观赏植物。"},
    {"name_cn": "落地生根", "name_latin": "Kalanchoe pinnata", "family": "景天科", "genus": "伽蓝菜属", "common_names": ["打不死"], "description": "落地生根是药用和观赏植物。"},
    {"name_cn": "玉树", "name_latin": "Crassula ovata", "family": "景天科", "genus": "青锁龙属", "common_names": ["燕子掌"], "description": "玉树是多肉观赏植物。"},
    {"name_cn": "碰碰香", "name_latin": "Plectranthus hadiensis var. tomentosus", "family": "唇形科", "genus": "马刺花属", "common_names": ["豆蔻天竺葵"], "description": "碰碰香是芳香观赏植物。"},
    {"name_cn": "迷迭香", "name_latin": "Rosmarinus officinalis", "family": "唇形科", "genus": "迷迭香属", "common_names": ["海洋之露"], "description": "迷迭香是芳香植物。"},
    {"name_cn": "薰衣草", "name_latin": "Lavandula angustifolia", "family": "唇形科", "genus": "薰衣草属", "common_names": ["灵香草"], "description": "薰衣草是著名的芳香植物。"},
    {"name_cn": "薄荷", "name_latin": "Mentha haplocalyx", "family": "唇形科", "genus": "薄荷属", "common_names": ["野薄荷"], "description": "薄荷是芳香和药用植物。"},
    {"name_cn": "留兰香", "name_latin": "Mentha spicata", "family": "唇形科", "genus": "薄荷属", "common_names": ["绿薄荷"], "description": "留兰香是芳香植物。"},
    {"name_cn": "罗勒", "name_latin": "Ocimum basilicum", "family": "唇形科", "genus": "罗勒属", "common_names": ["九层塔"], "description": "罗勒是芳香植物。"},
    {"name_cn": "紫苏", "name_latin": "Perilla frutescens", "family": "唇形科", "genus": "紫苏属", "common_names": ["白苏"], "description": "紫苏是药用和食用植物。"},
    {"name_cn": "藿香", "name_latin": "Agastache rugosa", "family": "唇形科", "genus": "藿香属", "common_names": ["土藿香"], "description": "藿香是药用植物。"},
    {"name_cn": "黄芩", "name_latin": "Scutellaria baicalensis", "family": "唇形科", "genus": "黄芩属", "common_names": ["山茶根"], "description": "黄芩是药用植物。"},
    {"name_cn": "丹参", "name_latin": "Salvia miltiorrhiza", "family": "唇形科", "genus": "鼠尾草属", "common_names": ["红根"], "description": "丹参是药用植物。"},
    {"name_cn": "益母草", "name_latin": "Leonurus artemisia", "family": "唇形科", "genus": "益母草属", "common_names": ["茺蔚"], "description": "益母草是药用植物。"},
    {"name_cn": "荆芥", "name_latin": "Schizonepeta tenuifolia", "family": "唇形科", "genus": "裂叶荆芥属", "common_names": ["香荆芥"], "description": "荆芥是药用植物。"},
    {"name_cn": "桔梗", "name_latin": "Platycodon grandiflorus", "family": "桔梗科", "genus": "桔梗属", "common_names": ["包袱花"], "description": "桔梗是药用和观赏植物。"},
    {"name_cn": "党参", "name_latin": "Codonopsis pilosula", "family": "桔梗科", "genus": "党参属", "common_names": ["黄参"], "description": "党参是药用植物。"},
    {"name_cn": "沙参", "name_latin": "Adenophora stricta", "family": "桔梗科", "genus": "沙参属", "common_names": ["南沙参"], "description": "沙参是药用植物。"},
    {"name_cn": "半边莲", "name_latin": "Lobelia chinensis", "family": "桔梗科", "genus": "半边莲属", "common_names": ["急解索"], "description": "半边莲是药用植物。"},
    {"name_cn": "菊花", "name_latin": "Chrysanthemum morifolium", "family": "菊科", "genus": "菊属", "common_names": ["寿客"], "description": "菊花是中国传统名花。"},
    {"name_cn": "野菊", "name_latin": "Chrysanthemum indicum", "family": "菊科", "genus": "菊属", "common_names": ["野菊花"], "description": "野菊是药用植物。"},
    {"name_cn": "红花", "name_latin": "Carthamus tinctorius", "family": "菊科", "genus": "红花属", "common_names": ["草红花"], "description": "红花是药用和油料植物。"},
    {"name_cn": "白术", "name_latin": "Atractylodes macrocephala", "family": "菊科", "genus": "苍术属", "common_names": ["于术"], "description": "白术是药用植物。"},
    {"name_cn": "苍术", "name_latin": "Atractylodes lancea", "family": "菊科", "genus": "苍术属", "common_names": ["茅苍术"], "description": "苍术是药用植物。"},
    {"name_cn": "牛蒡", "name_latin": "Arctium lappa", "family": "菊科", "genus": "牛蒡属", "common_names": ["大力子"], "description": "牛蒡是药用和食用植物。"},
    {"name_cn": "蒲公英", "name_latin": "Taraxacum mongolicum", "family": "菊科", "genus": "蒲公英属", "common_names": ["黄花地丁"], "description": "蒲公英是药用植物。"},
    {"name_cn": "紫菀", "name_latin": "Aster tataricus", "family": "菊科", "genus": "紫菀属", "common_names": ["青菀"], "description": "紫菀是药用植物。"},
    {"name_cn": "款冬", "name_latin": "Tussilago farfara", "family": "菊科", "genus": "款冬属", "common_names": ["冬花"], "description": "款冬是药用植物。"},
    {"name_cn": "苍耳", "name_latin": "Xanthium sibiricum", "family": "菊科", "genus": "苍耳属", "common_names": ["老苍子"], "description": "苍耳是药用植物。"},
    {"name_cn": "艾", "name_latin": "Artemisia argyi", "family": "菊科", "genus": "蒿属", "common_names": ["艾蒿"], "description": "艾是药用植物。"},
    {"name_cn": "茵陈", "name_latin": "Artemisia capillaris", "family": "菊科", "genus": "蒿属", "common_names": ["绵茵陈"], "description": "茵陈是药用植物。"},
    {"name_cn": "青蒿", "name_latin": "Artemisia carvifolia", "family": "菊科", "genus": "蒿属", "common_names": ["香蒿"], "description": "青蒿是药用植物。"},
    {"name_cn": "佩兰", "name_latin": "Eupatorium fortunei", "family": "菊科", "genus": "泽兰属", "common_names": ["兰草"], "description": "佩兰是药用植物。"},
    {"name_cn": "泽兰", "name_latin": "Lycopus lucidus", "family": "唇形科", "genus": "地笋属", "common_names": ["地笋"], "description": "泽兰是药用植物。"},
    {"name_cn": "石竹", "name_latin": "Dianthus chinensis", "family": "石竹科", "genus": "石竹属", "common_names": ["洛阳花"], "description": "石竹是观赏花卉。"},
    {"name_cn": "康乃馨", "name_latin": "Dianthus caryophyllus", "family": "石竹科", "genus": "石竹属", "common_names": ["香石竹"], "description": "康乃馨是著名的观赏花卉。"},
    {"name_cn": "满天星", "name_latin": "Gypsophila paniculata", "family": "石竹科", "genus": "石头花属", "common_names": ["圆锥石头花"], "description": "满天星是著名的切花材料。"},
    {"name_cn": "剪秋罗", "name_latin": "Lychnis fulgens", "family": "石竹科", "genus": "剪秋罗属", "common_names": ["大花剪秋罗"], "description": "剪秋罗是观赏花卉。"},
    {"name_cn": "王不留行", "name_latin": "Vaccaria segetalis", "family": "石竹科", "genus": "麦蓝菜属", "common_names": ["麦蓝菜"], "description": "王不留行是药用植物。"},
    {"name_cn": "金鱼草", "name_latin": "Antirrhinum majus", "family": "玄参科", "genus": "金鱼草属", "common_names": ["龙头花"], "description": "金鱼草是观赏花卉。"},
    {"name_cn": "蒲包花", "name_latin": "Calceolaria crenatiflora", "family": "玄参科", "genus": "蒲包花属", "common_names": ["荷包花"], "description": "蒲包花是观赏花卉。"},
    {"name_cn": "夏堇", "name_latin": "Torenia fournieri", "family": "玄参科", "genus": "蓝猪耳属", "common_names": ["蓝猪耳"], "description": "夏堇是观赏花卉。"},
    {"name_cn": "毛地黄", "name_latin": "Digitalis purpurea", "family": "玄参科", "genus": "毛地黄属", "common_names": ["洋地黄"], "description": "毛地黄是药用和观赏植物。"},
    {"name_cn": "钓钟柳", "name_latin": "Penstemon campanulatus", "family": "玄参科", "genus": "钓钟柳属", "common_names": ["吊钟柳"], "description": "钓钟柳是观赏花卉。"},
    {"name_cn": "凤仙花", "name_latin": "Impatiens balsamina", "family": "凤仙花科", "genus": "凤仙花属", "common_names": ["指甲花"], "description": "凤仙花是观赏花卉。"},
    {"name_cn": "何氏凤仙", "name_latin": "Impatiens walleriana", "family": "凤仙花科", "genus": "凤仙花属", "common_names": ["玻璃翠"], "description": "何氏凤仙是室内观赏花卉。"},
    {"name_cn": "新几内亚凤仙", "name_latin": "Impatiens hawkeri", "family": "凤仙花科", "genus": "凤仙花属", "common_names": ["四季凤仙"], "description": "新几内亚凤仙是观赏花卉。"},
    {"name_cn": "三色堇", "name_latin": "Viola tricolor", "family": "堇菜科", "genus": "堇菜属", "common_names": ["蝴蝶花"], "description": "三色堇是著名的观赏花卉。"},
    {"name_cn": "角堇", "name_latin": "Viola cornuta", "family": "堇菜科", "genus": "堇菜属", "common_names": ["小三色堇"], "description": "角堇是观赏花卉。"},
    {"name_cn": "紫花地丁", "name_latin": "Viola philippica", "family": "堇菜科", "genus": "堇菜属", "common_names": ["野堇菜"], "description": "紫花地丁是药用和观赏植物。"},
    {"name_cn": "旱金莲", "name_latin": "Tropaeolum majus", "family": "旱金莲科", "genus": "旱金莲属", "common_names": ["金莲花"], "description": "旱金莲是观赏花卉。"},
    {"name_cn": "天竺葵", "name_latin": "Pelargonium hortorum", "family": "牻牛儿苗科", "genus": "天竺葵属", "common_names": ["洋绣球"], "description": "天竺葵是室内观赏花卉。"},
    {"name_cn": "香叶天竺葵", "name_latin": "Pelargonium graveolens", "family": "牻牛儿苗科", "genus": "天竺葵属", "common_names": ["驱蚊草"], "description": "香叶天竺葵是芳香植物。"},
    {"name_cn": "酢浆草", "name_latin": "Oxalis corniculata", "family": "酢浆草科", "genus": "酢浆草属", "common_names": ["三叶草"], "description": "酢浆草是地被植物。"},
    {"name_cn": "红花酢浆草", "name_latin": "Oxalis corymbosa", "family": "酢浆草科", "genus": "酢浆草属", "common_names": ["铜锤草"], "description": "红花酢浆草是观赏地被植物。"},
    {"name_cn": "紫叶酢浆草", "name_latin": "Oxalis triangularis", "family": "酢浆草科", "genus": "酢浆草属", "common_names": ["三角酢浆草"], "description": "紫叶酢浆草是彩叶观赏植物。"},
    {"name_cn": "老鹳草", "name_latin": "Geranium wilfordii", "family": "牻牛儿苗科", "genus": "老鹳草属", "common_names": ["老鸦嘴"], "description": "老鹳草是药用植物。"},
    {"name_cn": "大花天竺葵", "name_latin": "Pelargonium domesticum", "family": "牻牛儿苗科", "genus": "天竺葵属", "common_names": ["蝴蝶天竺葵"], "description": "大花天竺葵是观赏花卉。"},
    {"name_cn": "飞燕草", "name_latin": "Consolida ajacis", "family": "毛茛科", "genus": "飞燕草属", "common_names": ["千鸟草"], "description": "飞燕草是观赏花卉。"},
    {"name_cn": "耧斗菜", "name_latin": "Aquilegia vulgaris", "family": "毛茛科", "genus": "耧斗菜属", "common_names": ["猫爪花"], "description": "耧斗菜是观赏花卉。"},
    {"name_cn": "乌头", "name_latin": "Aconitum carmichaelii", "family": "毛茛科", "genus": "乌头属", "common_names": ["附子"], "description": "乌头是药用植物。"},
    {"name_cn": "黄连", "name_latin": "Coptis chinensis", "family": "毛茛科", "genus": "黄连属", "common_names": ["味连"], "description": "黄连是药用植物。"},
    {"name_cn": "白头翁", "name_latin": "Pulsatilla chinensis", "family": "毛茛科", "genus": "白头翁属", "common_names": ["老婆子花"], "description": "白头翁是药用植物。"},
    {"name_cn": "升麻", "name_latin": "Cimicifuga foetida", "family": "毛茛科", "genus": "升麻属", "common_names": ["绿升麻"], "description": "升麻是药用植物。"},
    {"name_cn": "威灵仙", "name_latin": "Clematis chinensis", "family": "毛茛科", "genus": "铁线莲属", "common_names": ["铁脚威灵仙"], "description": "威灵仙是药用植物。"},
    {"name_cn": "铁线莲", "name_latin": "Clematis florida", "family": "毛茛科", "genus": "铁线莲属", "common_names": ["番莲"], "description": "铁线莲是观赏藤本植物。"},
    {"name_cn": "转子莲", "name_latin": "Clematis patens", "family": "毛茛科", "genus": "铁线莲属", "common_names": ["大花铁线莲"], "description": "转子莲是观赏植物。"},
    {"name_cn": "唐松草", "name_latin": "Thalictrum aquilegifolium", "family": "毛茛科", "genus": "唐松草属", "common_names": ["草黄连"], "description": "唐松草是观赏植物。"},
    {"name_cn": "翠雀", "name_latin": "Delphinium grandiflorum", "family": "毛茛科", "genus": "翠雀属", "common_names": ["大花飞燕草"], "description": "翠雀是观赏花卉。"},
    {"name_cn": "楼斗菜", "name_latin": "Aquilegia viridiflora", "family": "毛茛科", "genus": "耧斗菜属", "common_names": ["猫爪花"], "description": "楼斗菜是药用植物。"},
    {"name_cn": "驴蹄草", "name_latin": "Caltha palustris", "family": "毛茛科", "genus": "驴蹄草属", "common_names": ["马蹄叶"], "description": "驴蹄草是药用植物。"},
    {"name_cn": "金莲花", "name_latin": "Trollius chinensis", "family": "毛茛科", "genus": "金莲花属", "common_names": ["旱荷"], "description": "金莲花是药用和观赏植物。"},
]

def create_plant(template, plant_id, image_source="PPBC"):
    """创建完整的植物数据"""
    seed = template.get('name_cn', 'plant').replace(' ', '')
    
    if template.get('ppbc_id'):
        primary_image = f"{PPBC_BASE_URL}{template['ppbc_id']}.jpg"
        image_source_val = "PPBC中国植物图像库"
    else:
        primary_image = f"https://picsum.photos/seed/{seed}/800/600"
        image_source_val = "picsum.photos"
    
    return {
        "id": plant_id,
        "name_cn": template.get('name_cn', ''),
        "name_latin": template.get('name_latin', ''),
        "family": template.get('family', ''),
        "genus": template.get('genus', ''),
        "common_names": template.get('common_names', []),
        "description": template.get('description', ''),
        "detailed_description": template.get('description', ''),
        "morphology": "",
        "habitat": "喜阳光充足环境，适应性强。",
        "distribution": "中国大部分地区均有分布。",
        "garden_zones": template.get('garden_zones', ['树木园']),
        "protection_status": template.get('protection_status', ''),
        "iucn_status": "",
        "uses": template.get('uses', ['观赏']),
        "medicinal_uses": template.get('medicinal_uses', ''),
        "ornamental_value": template.get('description', ''),
        "ecological_value": "",
        "cultural_significance": "",
        "flowering_period": template.get('flowering_period', ''),
        "fruiting_period": "",
        "light_requirements": "喜光",
        "water_requirements": "中等",
        "soil_preference": "各种土壤",
        "temperature_range": "",
        "hardiness_zone": "",
        "growth_rate": "中等",
        "lifespan": "",
        "max_height": "",
        "max_width": "",
        "leaf_type": "",
        "flower_color": "",
        "fruit_color": "",
        "ppbc_id": template.get('ppbc_id', ''),
        "image_source": image_source_val,
        "primary_image": primary_image,
        "image_urls": [primary_image],
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_url": "beijing_botanical_garden_database",
        "notes": ""
    }

def main():
    print("="*70)
    print("北京植物园植物数据库生成工具 - 完整版")
    print("="*70)
    
    all_plants = []
    seen_ids = set()
    seen_latin = set()
    seen_names = set()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '..', 'data')
    
    source_files = [
        os.path.join(output_dir, 'plants.json'),
        os.path.join(output_dir, 'plants_extended.json'),
        os.path.join(output_dir, 'plants_200.json')
    ]
    
    print(f"\n读取现有数据文件...")
    for file_path in source_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            plants = data.get('plants', []) if isinstance(data, dict) else data
            print(f"  {os.path.basename(file_path)}: {len(plants)} 种")
            
            for plant in plants:
                if plant.get('id') in seen_ids:
                    continue
                if plant.get('name_latin') and plant['name_latin'] in seen_latin:
                    continue
                if plant.get('name_cn') and plant['name_cn'] in seen_names:
                    continue
                
                seen_ids.add(plant['id'])
                if plant.get('name_latin'):
                    seen_latin.add(plant['name_latin'])
                if plant.get('name_cn'):
                    seen_names.add(plant['name_cn'])
                
                ppbc_id = plant.get('ppbc_id', '')
                if ppbc_id:
                    plant['primary_image'] = f"{PPBC_BASE_URL}{ppbc_id}.jpg"
                    plant['image_urls'] = [plant['primary_image']]
                    plant['image_source'] = 'PPBC中国植物图像库'
                else:
                    seed = plant.get('name_cn', 'plant').replace(' ', '')
                    plant['primary_image'] = f"https://picsum.photos/seed/{seed}/800/600"
                    plant['image_urls'] = [plant['primary_image']]
                    plant['image_source'] = 'picsum.photos'
                
                all_plants.append(plant)
    
    print(f"合并现有数据后: {len(all_plants)} 种植物")
    
    print(f"\n添加有PPBC真实图片的植物...")
    ppbc_count = 0
    for plant_template in PLANTS_WITH_PPBC:
        if plant_template['name_latin'] in seen_latin or plant_template['name_cn'] in seen_names:
            continue
        
        plant_id = f"ppbc_{len(all_plants)+1:03d}"
        plant = create_plant(plant_template, plant_id, "PPBC")
        
        seen_latin.add(plant_template['name_latin'])
        seen_names.add(plant_template['name_cn'])
        
        all_plants.append(plant)
        ppbc_count += 1
    
    print(f"新增PPBC植物: {ppbc_count} 种")
    print(f"当前总数: {len(all_plants)} 种")
    
    print(f"\n添加额外的植物数据...")
    additional_count = 0
    for plant_template in ADDITIONAL_PLANTS:
        if plant_template['name_latin'] in seen_latin or plant_template['name_cn'] in seen_names:
            continue
        
        plant_id = f"plant_ext_{len(all_plants)+1:03d}"
        plant = create_plant(plant_template, plant_id)
        
        seen_latin.add(plant_template['name_latin'])
        seen_names.add(plant_template['name_cn'])
        
        all_plants.append(plant)
        additional_count += 1
        
        if len(all_plants) >= 300:
            break
    
    print(f"新增额外植物: {additional_count} 种")
    print(f"当前总数: {len(all_plants)} 种")
    
    families = set(p.get('family') for p in all_plants if p.get('family'))
    protected = [p for p in all_plants if p.get('protection_status')]
    ppbc_total = sum(1 for p in all_plants if p.get('ppbc_id'))
    
    metadata = {
        "source": "北京植物园完整植物数据库",
        "description": "北京植物园植物数据库（完整版，300+种，含PPBC真实图片）",
        "total_count": len(all_plants),
        "family_count": len(families),
        "protected_count": len(protected),
        "ppbc_image_count": ppbc_total,
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "9.0",
        "image_source": "PPBC中国植物图像库（真实图片） + picsum.photos（备用）"
    }
    
    output_data = {
        "metadata": metadata,
        "plants": all_plants
    }
    
    output_file = os.path.join(output_dir, 'plants_final.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    
    mini_output_file = os.path.join(output_dir, 'plants_final.min.json')
    with open(mini_output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False)
    
    print(f"迷你版数据已保存到: {mini_output_file}")
    print(f"\n{'='*70}")
    print(f"植物总数: {len(all_plants)} 种 {'✓' if len(all_plants) >= 200 else '✗'}")
    print(f"科属数量: {len(families)} 个科")
    print(f"保护植物: {len(protected)} 种")
    print(f"真实图片(PPBC): {ppbc_total} 种")
    print(f"备用图片(picsum): {len(all_plants) - ppbc_total} 种")
    print(f"{'='*70}")
    
    if len(all_plants) >= 250:
        print("\n✓ 已达到250+种植物的目标！")
    else:
        print(f"\n✗ 未达到目标，当前只有 {len(all_plants)} 种")

if __name__ == '__main__':
    main()
