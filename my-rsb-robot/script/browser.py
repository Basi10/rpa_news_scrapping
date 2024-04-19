from typing import Union
from urllib.parse import ParseResult
from RPA.Browser.Selenium import Selenium, By
from RPA.Robocorp.WorkItems import WorkItems
from script import logger

class BrowserAction:
    """
    Class for performing actions on a web browser.
    """
    
    def __init__(self, selenium: Selenium):
        """
        Initializes BrowserAction with a Selenium instance.
        
        Args:
            selenium (Selenium): Instance of Selenium.
        """
        self.selenium = selenium
        self.logger = logger.setup_logger(__name__, './output/browser_action.log')
    
    def connect(self, url: Union[str, ParseResult] = "https://gothamist.com/search"):
        """
        Connect to the browser and maximize the window.
        
        Args:
            url (Union[str, ParseResult], optional): URL to open in the browser. Defaults to "https://gothamist.com/search".
        """
        self.logger.info(f"Connecting to URL: {url}")
        self.selenium.set_selenium_timeout(1000)
        self.selenium.open_available_browser(url)
        self.selenium.maximize_browser_window()
    
    def retrieve_work_item(self, variable: str) -> str:
        """
        Retrieve the work item from the user.
        
        Args:
            variable (str): Variable name to retrieve.
        
        Returns:
            str: Retrieved work item.
        """
        self.logger.info(f"Retrieving work item for variable: {variable}")
        library = WorkItems()
        library.get_input_work_item()
        variables = library.get_work_item_variables()
        item = variables[variable]
        return item
        
    def search_initial(self):
        """
        Method to be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")
    
    def retrieve_description(self):
        """
        Method to be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")
    
    def retrieve_references(self):
        """
        Method to be implemented by subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")
    
    def close_browser(self):
        """
        Close the browser.
        """
        self.logger.info("Closing the browser")
        self.selenium.close_browser()


class GothamistAction(BrowserAction):    
    """
    Class for performing actions specific to Gothamist website.
    """
    
    def __init__(self, selenium: Selenium, url: Union[str, ParseResult]):
        """
        Initializes GothamistAction with a Selenium instance and URL.
        
        Args:
            selenium (Selenium): Instance of Selenium.
            url (Union[str, ParseResult]): URL of Gothamist website.
        """
        super().__init__(selenium)
        self.url = url

    def search_variable(self, variable: str):
        """
        Search for the variable in the search page.
        
        Args:
            variable (str): Variable to search.
        """
        self.logger.info(f"Searching for variable: {variable}")
        self.selenium.wait_until_element_is_visible("class:search-page-input", timeout=1000)
        self.selenium.input_text_when_element_is_visible("class:search-page-input", variable)
        self.selenium.click_element('class:search-page-button')
        self.selenium.wait_until_element_is_visible('class:h2')
    
    def retrieve_description(self) -> list:
        """
        Retrieve the description from the search page.
        
        Returns:
            list: List of descriptions.
        """
        self.logger.info("Retrieving descriptions")
        description = []
        desc = self.selenium.find_elements('class:card-slot')
        for div in desc:
            description.append(div.text)
        return description
    
    def retrieve_references(self) -> list:
        """
        Retrieve the links from the search page.
        
        Returns:
            list: List of links.
        """
        self.logger.info("Retrieving references")
        links = []
        reference = self.selenium.find_elements('class:card-title-link')
        for link in reference:
            links.append(link.get_attribute("href"))
        return links
    
    def retrieve_title(self):
        """
        Retrieve the title of the page.
        
        Returns:
            str: Title of the page.
        """
        self.logger.info("Retrieving title")
        self.selenium.go_to(self.url)
        self.selenium.wait_until_element_is_visible('class:h2')
        title = self.selenium.get_text('class:h2')
        return title
        
    def retrieve_image(self):
        """
        Retrieve the image from the page.
        
        Returns:
            str: Source URL of the image.
        """
        self.logger.info("Retrieving image")
        self.selenium.wait_until_element_is_visible('class:image-with-caption-wrapper')
        img = self.selenium.find_element('class:image-with-caption-wrapper')
        image_element = img.find_element(by=By.CLASS_NAME, value='image')
        image_source = image_element.get_attribute("src")
        return image_source
    
    def retrieve_date(self):
        """
        Retrieve the date from the page.
        
        Returns:
            str: Published date.
        """
        self.logger.info("Retrieving date")
        self.selenium.wait_until_element_is_visible('class:date-published')
        date = self.selenium.get_text('class:date-published')
        return date
