import scrapy
from pokescraper.items import Pokemon


class JoltikSpider(scrapy.Spider):
    name = "joltik"
    allowed_domains = ["bulbapedia.bulbagarden.net"]
    start_urls = ["https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"]

    def parse(self, response):
        pokemon = response.xpath("//table[contains(@class, 'roundy')]//tr//a/@href").getall()
        url_set = set()
        for poke in pokemon:
            if "Pok%C3%A9mon" in poke: 
                poke_url = 'https://bulbapedia.bulbagarden.net' + poke
                if poke_url not in url_set:
                    url_set.add(poke_url)
                    yield scrapy.Request(poke_url, callback=self.parse_poke_page)
            else:
                continue
            
    def parse_poke_page(self, response):
        pokemon = Pokemon()
        pokemon['pokedex_no'] = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/th/big/big/a/span/text()').get()
        pokemon['name'] = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/big/big/b/text()').get()
        
        types = response.xpath('//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr//b')
        pokemon['type1'] = types[0].xpath('string()').get()
        type2 = types[1].xpath('string()').get()
        if "Unknown" not in type2:
            pokemon['type2'] = type2
            
        stat_table = response.xpath('//*[descendant-or-self::span[contains(translate(@id, "STATS", "stats"), "stats")]]/following-sibling::table[1]')
        pokemon['hp'] = stat_table.xpath('./tbody/tr[3]/th/div[2]/text()').get()    
        pokemon['attack'] = stat_table.xpath('./tbody/tr[4]/th/div[2]/text()').get()
        pokemon['defense'] = stat_table.xpath('./tbody/tr[5]/th/div[2]/text()').get()
        pokemon['sp_attack'] = stat_table.xpath('./tbody/tr[6]/th/div[2]/text()').get()
        pokemon['sp_defense'] = stat_table.xpath('./tbody/tr[7]/th/div[2]/text()').get()
        pokemon['speed'] = stat_table.xpath('./tbody/tr[8]/th/div[2]/text()').get()
        pokemon['total_bst'] = stat_table.xpath('./tbody/tr[9]/th/div[2]/text()').get()
        
        yield pokemon
        
