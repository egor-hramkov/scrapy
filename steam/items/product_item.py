from itemloaders.processors import Compose

import scrapy
from steam.utils import list_to_str

import re


def cast_reviews_to_int(x: list) -> int:
    """Вытягивает число из сырых данных об отзыве"""
    return int(re.search(r'\d+', x[0]).group())


class ProductItem(scrapy.Item):
    app_name = scrapy.Field()
    specs = scrapy.Field(output_processor=Compose(list_to_str))
    n_reviews = scrapy.Field(
        output_processor=Compose(cast_reviews_to_int)
    )
    positive_reviews = scrapy.Field(
        output_processor=Compose(cast_reviews_to_int)
    )
    negative_reviews = scrapy.Field(
        output_processor=Compose(cast_reviews_to_int)
    )
    positive_percent = scrapy.Field()
    negative_percent = scrapy.Field()
