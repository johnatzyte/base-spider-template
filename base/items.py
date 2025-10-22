import attrs

# define classes using attrs - setup for my test e-commerce site

@attrs.define
class ProductItem:
    name: str
    brand: str
    category: str
    price: float
    sku: str
    gtin: str
    stock: int
    dimensions: str
    rating: str
    tags: list[str]
    url: str

@attrs.define
class ListItem:
    product_urls: list[str]
    next_page_url: str | None = None
    url: str