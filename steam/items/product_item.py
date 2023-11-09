from itemloaders.processors import MapCompose, Compose

import scrapy
from steam.utils import str_to_int, StripText, list_to_str


class ProductItem(scrapy.Item):
    app_name = scrapy.Field()
    specs = scrapy.Field(output_processor=Compose(list_to_str))
    n_reviews = scrapy.Field(
        output_processor=Compose(
            MapCompose(
                lambda x: x.replace('(', ''),
                lambda x: x.replace(')', ''),
                lambda x: x.split()[0],
                str_to_int),
            max
        )
    )
