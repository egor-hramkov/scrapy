from typing import Any
import time

from scrapy import Selector, Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.spiders import Spider
from steam.items.product_item import ProductItem
from steam.items.product_item_loader import ProductItemLoader
from steam.enums import SelectorsEnum
from steam.utils import parse_time


class ProductsSpider(Spider):
    base_url = 'https://store.steampowered.com/search/results/?query&start={}&count={}&sort_by=Released_DESC&infinite=1'
    name = 'products'
    start_urls = [base_url.format(0, 50)]
    allowed_domains = ["steampowered.com"]
    start = 0
    count = 50
    skip_n_games = 0
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../products.csv',
        'FEEDS': {
            'products.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    def __init__(self, skip_n_games: int = 0, **kwargs):
        self.skip_n_games = skip_n_games
        if skip_n_games != 0:
            self.custom_settings['FEEDS']['products.csv']['overwrite'] = False
            self.start = skip_n_games
            self.start_urls = [self.base_url.format(self.start, self.count)]
        super().__init__(**kwargs)

    def parse(self, response: Response, **kwargs: Any):
        data = response.json().get('results_html', '')
        games = Selector(text=data).css('a').getall()
        for game in games:
            game_url = Selector(text=game).css('a ::attr(href)').extract_first()
            request = Request(url=game_url, callback=self.parse_product)
            yield request
        self.start += 50
        if self.start >= 100:
            return
        main_request = Request(
            url=self.base_url.format(self.start, self.count),
            callback=self.parse
        )
        yield main_request

    def parse_product(self, response) -> ProductItem:
        """Основной метод парсинга игр"""

        loader = ProductItemLoader(item=ProductItem(), response=response)
        loader.add_css('app_name', SelectorsEnum.APP_NAME_CSS.value)
        loader.add_css('specs', SelectorsEnum.SPECS_CSS.value)
        loader.add_css('n_reviews', SelectorsEnum.N_REVIEWS_CSS.value)
        loader.add_css('positive_reviews', SelectorsEnum.POSITIVE_REVIEWS_CSS.value)
        loader.add_css('negative_reviews', SelectorsEnum.NEGATIVE_REVIEWS_CSS.value)
        data: ProductItem = loader.load_item()
        self._post_proccesing(data)
        return data

    def _post_proccesing(self, data: ProductItem) -> ProductItem:
        """Пост обработка очищенных данных"""
        data['n_reviews'] = data.get('n_reviews', 0)
        data['positive_reviews'] = data.get('positive_reviews', 0)
        data['negative_reviews'] = data.get('negative_reviews', 0)
        data['positive_percent'] = int(data['positive_reviews'] / data['n_reviews'] * 100) if data['n_reviews'] != 0 else 0
        data['negative_percent'] = int(data['negative_reviews'] / data['n_reviews'] * 100) if data['n_reviews'] != 0 else 0
        return data


if __name__ == '__main__':
    print("Введите количество игр которое хотите пропустить: ")
    skip_n_games = int(input())

    start_time = time.time()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ProductsSpider, skip_n_games)
    process.start()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Время парсинга: ", parse_time(elapsed_time))
