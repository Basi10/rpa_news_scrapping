class Selector:
    TITLE = "xpath://h1[contains(@class,'h2')]"
    DATE = "xpath://p[@class='type-caption']"
    NEWS_NUMBER = "xpath://div[@class='search-page-results pt-2']/span/strong"
    IMAGE = "xpath://div[@class='image-with-caption-wrapper']//img"
    IMAGE_NAME = "xpath://div[contains(@class,'flexible-link')][contains(@class,'image-with-caption-credit-link')]"
    LINKS = "xpath://a[contains(@class,'card-title-link')]"
    DESCRIPTION = "xpath://p[@class='desc']"
    SEARCH_INPUT = "xpath://input[@class='search-page-input']"
    SEARCH_BUTTON = "xpath://button[contains (@class,'search-page-button')]"


class Directories:
    IMAGE_DIRECTORY = './output/'
    LOG_DIRECTORY = './output/browser_action.log'
    EXCEL_DIRECTORY = './output/'
    EXCEL_FILE_EXT = ".xlsx"
    SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]


class URL:
    GOTHAMIST_URL = 'https://gothamist.com/search'
