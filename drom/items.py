




















# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Поле с ID  ????
# Процессоры на вход и на выход, на вход наверно подавать целыми кусками и регулярками вытакивать 
# Логгирование, ссылку, если есть нулевые поля выдавать ошибку 
import scrapy
from scrapy.loader.processors import Compose, Identity, Join
import re

def trans_refine(string):
  a = {
    'АКПП':'AT',
    'МКПП':'MT',
    'вариатор':'CVT',
    'робот':'AMT'
    }
  for key in a.keys():
    if key in string:
      return a[key]

def date_refine(string):
  a = re.sub('\d{2}[.]',  '', string)
  return a    

def kvts(string):
  kvts = ''
  for i in string:
    if i.isdigit():
      kvts+=i
    else: pass
  return round(int(kvts)*0.7355)

class DromItem(scrapy.Item):    
    manufacturer = scrapy.Field()
    model = scrapy.Field()
    region = scrapy.Field()
    generation = scrapy.Field()
    rest = scrapy.Field()
    production_year = scrapy.Field()
    engine_vol = scrapy.Field()
    trans = scrapy.Field()
    fuel_type = scrapy.Field()
    privod = scrapy.Field()
    frametype = scrapy.Field()
    frames = scrapy.Field()
    engine = scrapy.Field()
    kvts = scrapy.Field()
    qubesant = scrapy.Field()
    kuzov = scrapy.Field()
   
  
#   class DromItem(scrapy.Item):    
#     manufacturer = scrapy.Field(output_processor=Join())
#     model = scrapy.Field(output_processor=Join())
#     region = scrapy.Field(output_processor=Join())
#     generation = scrapy.Field(
#         output_processor=Join())
#     rest = scrapy.Field(output_processor=Join())
#     production_year = scrapy.Field(
#         input_processor=Join(),
#         output_processor=Identity(),
#     )
#     engine_vol = scrapy.Field(
#         input_processor=Compose(lambda v:v[:3]),
#         output_processor=Identity(),
#         )
#     trans = scrapy.Field(
#         input_processor=Join(),
#         output_processor=Compose(trans_refine),
#     )
#     fuel_type = scrapy.Field()
#     privod = scrapy.Field()
#     frametype = scrapy.Field()
#     frames = scrapy.Field()
#     engine = scrapy.Field()
#     kvts = scrapy.Field(
#         input_processor=Compose(kvts),
#         output_processor=Identity(),
#     )
#     qubesant = scrapy.Field()
#     kuzov = scrapy.Field()
   
