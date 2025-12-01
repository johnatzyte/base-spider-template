from typing import List, Optional

from base.items import ListItem, ProductItem
from price_parser import Price
from web_poet import Returns, WebPage, field, handle_urls


@handle_urls("ooshn.com")
class OoshnComProductItemPage(WebPage, Returns[ProductItem]):
    @field
    def name(self) -> str:
        return self.css("h2#product-title::text").get()

    @field
    def brand(self) -> Optional[str]:
        return self.css("span.meta-brand::text").get()

    @field
    def category(self) -> Optional[str]:
        return self.css("a.meta-category::text").get()

    @field
    def price(self) -> Optional[float]:
        price_text = self.css(
            "#product-price span:not(.text-decoration-line-through)::text"
        ).get()
        if not price_text:
            return None
        price = Price.fromstring(price_text)
        return price.amount_float

    @field
    def sku(self) -> Optional[str]:
        return self.css("span.meta-sku::text").get()

    @field
    def gtin(self) -> Optional[str]:
        return self.css(".spec-gtin .spec-value::text").get()

    @field
    def stock(self) -> Optional[int]:
        stock_text = self.css(".stock-qty::text").get()
        if stock_text:
            try:
                return int(stock_text)
            except (ValueError, TypeError):
                return None
        return None

    @field
    def dimensions(self) -> Optional[str]:
        return self.css(".spec-dimensions .spec-value::text").get()

    @field
    def rating(self) -> Optional[str]:
        return self.css("li.spec-rating span.spec-value::text").get()

    @field
    def tags(self) -> Optional[List[str]]:
        """
        Extracts product tags from the page.
        """
        tags_list = self.css("#product-tags .badge--tag::text").getall()
        return tags_list or None

    @field
    def url(self) -> str:
        """
        Returns the canonical URL of the page.
        """
        return str(self.response.url)


@handle_urls("ooshn.com")
class OoshnComListItemPage(WebPage, Returns[ListItem]):
    @field
    def product_urls(self) -> List[str]:
        """
        Extracts product URLs from the listing page.
        """
        urls = self.css("div.card-body h5.card-title a::attr(href)").getall()
        return [self.urljoin(url) for url in urls]

    @field
    def next_page_url(self) -> Optional[str]:
        next_page_href = self.css('a[aria-label="Next"]::attr(href)').get()
        if next_page_href:
            return self.urljoin(next_page_href)
        return None

    @field
    def url(self) -> str:
        return str(self.response.url)
