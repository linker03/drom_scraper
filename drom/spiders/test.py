import scrapy
from scrapy.spiders import CrawlSpider
from drom.items import DromItem
from scrapy.loader import ItemLoader
import re
import time


class Dromspider(CrawlSpider):
  name = 'drom_test'
  start_urls = ['https://www.drom.ru/catalog/mitsubishi/']
  #start_urls = ['https://www.drom.ru/catalog/mitsubishi/lancer/']
  
  
  custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
  
  
  def second_floor(self, response, item):
    all_links = response.xpath('//div[@data-target-bind]//a[@href]')
    for a in all_links:  
      il = ItemLoader(DromItem(item), selector = a)
      il.add_xpath('region', '../../@data-target-bind')    
      il.add_xpath('production_year', './/span/text()[2]')
      time.sleep(0.75)
      yield il.load_item()
  
    
  
  def parse(self, response):
    
    all_links = response.xpath('//div[contains(@class,"b-selectCars__section")]//./a')
    for link in all_links[:3]:
      il = ItemLoader(DromItem(), selector=link)
      il.add_value('manufacturer', 'Mitsubishi')
      il.add_xpath('model', './/text()')
      lin = response.urljoin(link.xpath('.//@href').get())
      item = il.load_item()
      time.sleep(0.75)
      yield  scrapy.Request(lin, callback=self.second_floor, cb_kwargs=dict(item=item.copy())) 
  

