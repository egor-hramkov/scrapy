from itemloaders.processors import TakeFirst

from scrapy.loader import ItemLoader


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
