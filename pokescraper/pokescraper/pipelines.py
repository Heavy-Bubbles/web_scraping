# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class PokescraperPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
    
        # remove extra stuff from dex no
        dex_no = adapter.get('pokedex_no')
        if dex_no:
            # Use regular expression to find the first non-zero number
            match = re.search(r'#0*([1-9]\d*)', dex_no)
            if match:
                adapter['pokedex_no'] = int(match.group(1))
                
        # convert stats to int
        stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'total_bst']
        for stat in stats:
            stat_value = adapter.get(stat)
            adapter[stat] = int(stat_value)

        return item

