import scrapy
from scrapy.spiders import CrawlSpider
from drom.items import DromItem

import re
import time


class Dromspider(CrawlSpider):
  name = 'drom'
  start_urls = ['https://www.drom.ru/catalog/mitsubishi/']
  #start_urls = ['https://www.drom.ru/catalog/mitsubishi/lancer/']
  
  
  custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
  
  
  def fourth_floor(self, response, item):
    item = item
    item['qubesant'] = response.xpath('//td[contains(text(), "Объем двигателя")]/following::td/text()').get().strip()
    yield item
    
  
  def third_floor(self, response, item):
    item = item
    
    list_cars = response.xpath('//th[@colspan]')
    for cart in list_cars:
      car = cart.xpath('.//text()').get()
      for it in car.split(',').copy():
        if re.compile('\d[.]\d [л]').findall(it):
          item['engine_vol'] = it
        if 'л.с.' in it:
          item['kvts'] = it
        if 'привод' in it:
          item['privod'] = it
        for f in ['бензин', 'дизель']:
          if f in it:
            item['fuel_type'] = it
        for g in ['АКПП', 'МКПП', 'робот', 'вариатор']:
          if g in it:
            item['trans'] = it
      engine = cart.xpath('./../following::tr//*[contains(@href, "engine")]')
      item['engine'] = engine.xpath('.//text()').get()
      time.sleep(0.75)
      engine_link = response.urljoin(engine.xpath('.//@href').get())
      yield scrapy.Request(engine_link, callback=self.fourth_floor, dont_filter=True, cb_kwargs=dict(item=item.copy()))
  
  def second_floor(self, response, item):
    item = item
    all_links = response.xpath('//div[@data-target-bind]//a[@href]')
    for a in all_links:  
      deeper_link = response.urljoin(a.xpath('.//@href').get())
      item['region'] = a.xpath('../../@data-target-bind').get()
      raw_data = a.xpath('.//div[@class="b-info-block__descr"]//text()').getall()
      for i in raw_data.copy():
        if 'поколение' in i:
          item['generation'] = i
          raw_data.remove(i)
        if 'рестайлинг' in i:
          item['rest'] = i
          raw_data.remove(i)
        for fram in ['Седан', 'Универсал', 'Хэтчбек', 'Купе', 'Лифтбек', 'Открытый кузов', 'Джип', 'Минивэн']:
          if fram in i: 
            item['frametype'] = i.strip()
            raw_data.remove(i)
          
      item['frames'] = raw_data[-1] if raw_data else None
      item['production_year']  = a.xpath('.//span/text()[2]').get()
      
      item['kuzov'] = item['frames'].split(',')[0]  if item['frames'] else None #ku[ku.find('(')+1:ku.find(')')]
      
      time.sleep(0.75)
      yield scrapy.Request(deeper_link, callback=self.third_floor, cb_kwargs=dict(item=item.copy()))
    
  
  def parse(self, response):
    all_links = response.xpath('//div[contains(@class,"b-selectCars__section")]//./a')
    for link in all_links[:3]:
      item = DromItem()
      item['manufacturer'] = 'Mitsubishi'
      item['model'] = link.xpath('.//text()').get()
      lin = response.urljoin(link.xpath('.//@href').get())
      time.sleep(0.75)
      yield scrapy.Request(lin, callback=self.second_floor, cb_kwargs=dict(item=item.copy()))
  

