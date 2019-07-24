import requests
from lxml import etree
import time
import re
from tools.tools import data_to_json, get_img
import os


def get_url(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    url = html.xpath('//div[@class="section hero-result-box mod-bg clearfix"]/ul[@class="mod-iconlist"]/li/a/@href')
    url_list = ['https://db.18183.com/' + x for x in url]
    total = len(url_list)
    hero_list = []
    for index, u in enumerate(url_list):
        print('一共%d个, 正在抓取%d个' % (total, index + 1))
        data = get_info(u)
        hero_list.append(data)
        data_to_json(hero_list, 'hero')


def get_info(url):
    res = requests.get(url)
    time.sleep(1)
    hero_dict = {}
    html = etree.HTML(res.text)
    img_url = html.xpath('//div[@class="name"]/img/@data-original')[0]
    name = html.xpath('//div[@class="name"]//h1/text()')[0]
    tags = html.xpath('//div[@class="name"]/div[@class="name-box"]/p/a/text()')
    # base
    base = {}
    base_dls = html.xpath('//div[@class="base"]/dl')
    for base_dl in base_dls:
        key = base_dl.xpath('./dt/text()')[0]
        value = base_dl.xpath('./dd/text()')[0].strip().replace(' ', '')
        if key == '英雄礼包': continue
        base[key] = value
    # Attribute
    bast_attr = {}
    attr_dls = html.xpath('//div[@class="attr-list"]/dl')
    for attr_dl in attr_dls:
        key = attr_dl.xpath('./dt/text()')[0].replace('：', '')
        value_get = attr_dl.xpath('./dd/span/@class')[0]
        value = re.search('(\d+)', value_get)[1]
        bast_attr[key] = value
    hero_analysis = html.xpath('string(//div[@class="otherinfo-item"][1]//p/text())')
    background = html.xpath('string(//div[@class="otherinfo-item"][4]//p/text())')
    attr_dict = {}
    attrs = html.xpath('//div[@class="otherinfo-datapanel"]/ul/li//text()')
    for attr in attrs:
        result = re.search('(.*)：(.*)', attr)
        attr_dict[result[1]] = result[2]

    skills = html.xpath('//div[@class="skill-cont"]/div')
    skill_list = []
    for skill in skills:
        skill_name = skill.xpath('.//div[@class="title"]/span[1]/text()')[0]
        skill_attr = skill.xpath('.//div[@class="title"]/span[2]/text()')[0]
        skill_effect = ' '.join(skill.xpath('./p/text()'))
        skill_list.append({'name': skill_name, 'attr': skill_attr, 'effect': skill_effect.strip()})

    outfitting_dict = {}
    outfittings = html.xpath('//div[@class="collocation-box mod-bg"]')
    for outfitting in outfittings:
        key = outfitting.xpath('./div[@class="title"]/p/text()')[0]
        outfitting_list = outfitting.xpath('.//ul[@class="mod-iconlist"]/li/@data-id')
        outfitting_effect = outfitting.xpath('./div[@class="analysis"]/p/text()')[0]
        outfitting_dict[key] = {'list': outfitting_list, 'effect': outfitting_effect}

    inscription_dict = []
    inscriptions = html.xpath('//ul[@class="glyph-list"]/li')
    for inscription in inscriptions:
        inscription_name = inscription.xpath('.//p/text()')[0]
        inscription_attrs = inscription.xpath('.//dl[@class="info-panel"]/dd/text()')
        inscription_attr = [i.replace(' ', '').strip() for i in inscription_attrs]
        inscription_dict.append({'name': inscription_name, 'attr': inscription_attr})

    relationship_dict = {}
    relationships = html.xpath('//div[@class="section relation-hero-box mod-bg clearfix"]/div[@class="bd"]/div')
    for relationship in relationships:
        title = relationship.xpath('./div[@class="title"]/p/text()')[0]
        hero_name = relationship.xpath('./div[@class="content"]//a/@title')
        relationship_dict[title] = hero_name
    hero_dict['img_url'] = img_url
    hero_dict['name'] = name
    hero_dict['tags'] = tags
    hero_dict['bast_attr'] = bast_attr
    hero_dict['hero_analysis'] = hero_analysis
    hero_dict['background'] = background
    hero_dict['attrs'] = attr_dict
    hero_dict['skill_list'] = skill_list
    hero_dict['hero_analysis'] = hero_analysis
    hero_dict['base'] = base
    hero_dict['outfitting'] = outfitting_dict
    hero_dict['inscription'] = inscription_dict
    hero_dict['relationships'] = relationship_dict
    return hero_dict


def get_image(url):
    os.getcwd()
    pwd = get_img(url, os.getcwd())
    return pwd


if __name__ == '__main__':
    url = 'https://db.18183.com/wzry/'
    get_url(url)
