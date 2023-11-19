from enum import Enum


class SelectorsEnum(Enum):
    """Енам с селекторами"""
    APP_NAME_CSS = '.apphub_AppName ::text'
    SPECS_CSS = '#category_block > div > a > div.label ::text'
    N_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(2) > span ::text'
    POSITIVE_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(5) > span ::text'
    NEGATIVE_REVIEWS_CSS = '#reviews_filter_options > div:nth-child(1) > div.user_reviews_filter_menu_flyout > div > label:nth-child(8) > span ::text'
