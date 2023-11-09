from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from steam.items.product_item import ProductItem
from steam.items.product_item_loader import ProductItemLoader


class ProductsSpider(scrapy.spiders.CrawlSpider):
    name = 'products'
    start_urls = ["https://store.steampowered.com/search/?sort_by=Released_DESC"]
    allowed_domains = ["steampowered.com"]
    rules = [
        Rule(
            LinkExtractor(
                allow='/app/(.+)/',
                restrict_css='#search_result_container'
            ),
            callback='parse_product'
        ),
        Rule(
            LinkExtractor(
                allow='page=(d+)',
                restrict_css='.search_pagination_right'
            )
        )
    ]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'products.csv',
        'FEEDS': {
            'products.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    APP_NAME_CSS = '.apphub_AppName ::text'
    SPECS_CSS = '#category_block > div > a > div.label ::text'
    N_REVIEWS_CSS = '#review_histogram_rollup_section > div.user_reviews_summary_bar > div > span:nth-child(3) ::text'

    def parse_product(self, response) -> ProductItem:
        """Основной метод парсинга игр"""

        loader = ProductItemLoader(item=ProductItem(), response=response)
        loader.add_css('app_name', self.APP_NAME_CSS)
        loader.add_css('specs', self.SPECS_CSS)
        loader.add_css('n_reviews', self.N_REVIEWS_CSS)
        data: ProductItem = loader.load_item()
        data['n_reviews'] = data.get('n_reviews', 0)
        return data


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(ProductsSpider)
    process.start()
