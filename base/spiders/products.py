import scrapy
from base.items import ProductItem, ListItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    # setup for my test e-commerce site
    url: str = "https://ooshn.com/"

    async def start(self):
        yield scrapy.Request(url=self.url, callback=self.parse_list)

    async def parse_list(self, response, page:ListItem):
        for product_url in page.product_urls:
            yield response.follow(url=product_url, callback=self.parse_product)

        if page.next_page_url:
            yield response.follow(
                url=page.next_page_url,
                callback=self.parse_list
            )
    
    async def parse_product(self, _, product:ProductItem):
        yield product
