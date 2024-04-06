import scrapy
from chocolatescraper.itemloader import ChocolateProductLoader
from chocolatescraper.items import ChocolatescraperItem


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):     
        products = response.css('product-item')
        for product in products:
            chocolate_item = ChocolateProductLoader(item=ChocolatescraperItem(), selector=product)
            chocolate_item.add_css('name', 'a.product-item-meta__title::text')
            chocolate_item.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate_item.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate_item.load_item()
            
        next_page = response.css('a.pagination__nav-item ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)
