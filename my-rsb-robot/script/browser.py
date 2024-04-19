from typing import Union
from urllib.parse import ParseResult
from RPA.Browser.Selenium import Selenium, By
from RPA.Robocorp.WorkItems import WorkItems


class Broswer_Action:
    
    def __init__(self,selenium: Selenium):
        self.selenium = selenium
    
    def connect(self, url: Union[str, ParseResult] = "https://gothamist.com/search"):
        """
        Connect to the browser
        """
        self. selenium.set_selenium_timeout(1000)
        self.selenium.open_available_browser(url)
        self.selenium.maximize_browser_window()
    
    def retrieve_work_item(self, variable: str) -> str:
        """
        Retrieve the work item from the user
        """
        library = WorkItems()
        library.get_input_work_item()
        variables = library.get_work_item_variables()
        item = variables[variable]
        return item
        
    def search_initial(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def retrieve_description(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def retrieve_references(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def close_browser(self):
        self.selenium.close_browser()
        

class Gothamist_Action(Broswer_Action):    
    
    
    def __init__(self, selenium: Selenium, url: Union[str, ParseResult]):
        super().__init__(selenium)
        self.url = url

    def search_variable(self, variable: str):
        """
        Search for the variable in the search page
        """
        self.selenium.wait_until_element_is_visible("class:search-page-input", timeout=1000)
        self.selenium.input_text_when_element_is_visible("class:search-page-input", variable)
        self.selenium.click_element('class:search-page-button')
        self.selenium.wait_until_element_is_visible('class:h2')
    
    
    def retrieve_description(self) -> list:
        """
        Retrieve the description from the search page
        """
        description = []
        desc = self.selenium.find_elements('class:card-slot')
        for div in desc:
            description.append(div.text)
        return description
    
    def retrieve_references(self) -> list:
        """Retrieve the links from the search page"""
        links = []
        reference = self.selenium.find_elements('class:card-title-link')
        for link in reference:
            links.append(link.get_attribute("href"))
        return links
    
    def retrive_title(self):
        self.selenium.go_to(self.url)
        self.selenium.wait_until_element_is_visible('class:h2')
        title = self.selenium.get_text('class:h2')
        return title
        
    def retrieve_image(self):
        self.selenium.wait_until_element_is_visible('class:image-with-caption-wrapper')
        img = self.selenium.find_element('class:image-with-caption-wrapper')
        image_element = img.find_element(by=By.CLASS_NAME,value='image')
        image_source = image_element.get_attribute("src")
        return image_source
    
    def retrieve_date(self):
        self.selenium.wait_until_element_is_visible('class:date-published')
        date = self.selenium.get_text('class:date-published')
        return date
    

  
        