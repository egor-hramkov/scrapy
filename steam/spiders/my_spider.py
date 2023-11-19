from typing import Any

from scrapy import Selector, Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response, HtmlResponse
from scrapy.spiders import Spider
from steam.items.product_item import ProductItem
from steam.items.product_item_loader import ProductItemLoader


class ProductsSpider(Spider):
    base_url = 'https://store.steampowered.com/search/results/?query&start={}&count={}&sort_by=Released_DESC&infinite=1'
    name = 'products'
    start_urls = [base_url.format(50, 50)]
    allowed_domains = ["steampowered.com"]
    rules = []
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'products.csv',
        'FEEDS': {
            'products.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    APP_NAME_CSS = '.apphub_AppName ::text'
    SPECS_CSS = '#category_block > div > a > div.label ::text'
    N_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(2) > span ::text'
    POSITIVE_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(5) > span ::text'
    NEGATIVE_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(8) > span ::text'

    def parse(self, response: Response, **kwargs: Any):
        data = response.json().get('results_html', '')
        games = Selector(text=data).css('a').getall()
        for game in games:
            game_url = Selector(text=game).css('a ::attr(href)').extract_first()
            request = Request(url=game_url, callback=self.parse_product)
            yield request

    def parse_product(self, response) -> ProductItem:
        """Основной метод парсинга игр"""

        loader = ProductItemLoader(item=ProductItem(), response=response)
        loader.add_css('app_name', self.APP_NAME_CSS)
        loader.add_css('specs', self.SPECS_CSS)
        loader.add_css('n_reviews', self.N_REVIEWS_CSS)
        loader.add_css('positive_reviews', self.POSITIVE_REVIEWS_CSS)
        loader.add_css('negative_reviews', self.NEGATIVE_REVIEWS_CSS)
        data: ProductItem = loader.load_item()
        self._post_proccesing(data)
        return data

    def _post_proccesing(self, data: ProductItem) -> ProductItem:
        data['n_reviews'] = data.get('n_reviews', 0)
        data['positive_reviews'] = data.get('positive_reviews', 0)
        data['negative_reviews'] = data.get('negative_reviews', 0)
        data['positive_percent'] = data['positive_reviews'] / data['n_reviews'] * 100 if data['n_reviews'] != 0 else 0
        data['negative_percent'] = data['negative_reviews'] / data['n_reviews'] * 100 if data['n_reviews'] != 0 else 0
        return data


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(ProductsSpider)
    process.start()
