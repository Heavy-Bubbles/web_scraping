# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class PriceToUSDPipeline:
    
    gdpToUsdRate = 1.3
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # check price present
        if adapter.get('price'):
            
            # converting the price to a float
            floatPrice = float(adapter['price'])
            
            # converting the price from gdp to usd
            adapter['price'] = floatPrice * self.gdpToUsdRate
            
            return item
        
        else:
            # drop item if no price
            raise DropItem(f"Missing price in {item}")
        

class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set()
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item
    
