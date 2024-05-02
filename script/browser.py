from datetime import timedelta
from typing import Union, List, Any
from urllib.parse import ParseResult
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
import robocorp.log as logger
from script.exceptions import ElementInteractionError
from script.utils import (
    download_image,
    count_keyword,
    check_money)
from script.constants import (
    Selector,
    Directories,
    URL
)


class BrowserAction:
    """
    Class for performing actions on a web browser.
    """

    def __init__(self, selenium: Selenium, timeout_sec: int = 20):
        """
        Initializes BrowserAction with a Selenium instance.
        
        Args:
            selenium (Selenium): Instance of Selenium.
            timeout_sec (int, optional): Timeout in seconds.
        """
        self.selenium = selenium
        self.selenium.set_selenium_timeout(timedelta(seconds=timeout_sec))
        self.logger = logger
        self.library = WorkItems()

    def connect(self, url: Union[str, ParseResult] = None) -> None:
        """
        Connect to the browser and maximize the window.
        
        Args:
            url (Union[str, ParseResult], optional): URL to open in the browser.
        """
        if url is None:
            self.selenium.open_available_browser()
        else:
            self.logger.info(f"Connecting to URL: {url}")
            self.selenium.open_available_browser(url)

    def browse(self, url: Union[str, ParseResult]) -> None:
        """
        Browse a specific url after the browser is already open.

        Args:
            url (Union[str, ParseResult], optional): URL to open in the browser.
        """
        if url is not None:
            try:
                self.selenium.go_to(url)
            except Exception as e:
                self.logger.exception(f'Error opening url: {url} with the error: {e}')
                raise Exception(f'Error opening url: {url} with the error: {e}')
        else:
            self.logger.exception("URL cannot be None")

    def maximize(self):
        """
        Maximize the browser to the full screen size.
        """
        self.selenium.maximize_browser_window()

    def _click_element(self, locator: str) -> None:
        """
        Clicks the web element identified by the given locator.

        Args:
            locator (str): The locator of the web element to click.

        Returns:
            bool: True if the element was successfully clicked, False otherwise.
        """
        try:
            self.selenium.click_element(locator)
            self.logger.info("Button clicked")
        except Exception as e:
            self.logger.exception(f"Error clicking element: {e}")
            raise ElementInteractionError(f"Error clicking element: {e}")

    def _input_text(self, locator: str, text: str) -> None:
        """
        Enters text into the input field identified by the given locator.

        Args:
            locator (str): The locator of the input field.
            text (str): The text to enter into the input field.

        Returns:
            bool: True if the text was successfully entered, False otherwise.
        """
        try:
            self.selenium.input_text(locator, text)
            self.logger.info("Successfully entered input text")
        except Exception as e:
            self.logger.exception(f"Error entering text: {e}")
            raise ElementInteractionError(f"Error entering text: {e}")

    def _retrieve_elements(self, locator: str) -> List[Any]:
        """
        Retrieves a list of web elements identified by the given locator.
        If the elements are found, they are returned as a list of WebElements.
        If the elements are not found, an exception is raised.

        Args:
            locator (str): The locator of the web elements to retrieve.

        Returns:
            List[Any]: A list of web elements matching the locator.
        """
        try:
            elements = self.selenium.find_elements(locator)
            self.logger.info("Successfully retrieved elements")
            return elements
        except Exception as e:
            self.logger.exception(f"Error retrieving elements: {e}")
            raise ElementInteractionError(f"Error retrieving elements: {e}")

    def _retrieve_text(self, locator: str) -> str:
        """
        Retrieves the text passed into the input field identified by the given locator.
        If the elements are found, the text part of the element is returned as a string.
        If the elements are not found, an exception is raised.

        Args:
            locator (str): The locator of the web elements to retrieve.

        Returns:
            List[Any]: A list of web elements matching the locator.
        """
        try:
            self.logger.info("Retrieving text element")
            text = self.selenium.get_text(locator)
            self.logger.info("Successfully retrieved elements")
            return text
        except Exception as e:
            self.logger.exception(f"Error retrieving elements: {e}")
            raise ElementInteractionError(f"Error retrieving elements: {e}")

    def _handle_invalid_action(self, action: str) -> None:
        """
        Handles an invalid action by raising a ValueError.

        Args:
            action (str): The invalid action.

        Raises:
            ValueError: If an invalid action is provided.
        """
        raise ValueError(f"Invalid action: {action}")

    def element_interaction(self, locator: str, action: str, text: str = None) -> Union[bool, List]:
        """
        Perform interaction with a web element based on the specified action.

        Args: locator (str): The locator of the web element. action (str): The action to perform. Possible values are
        'click', 'input_text', 'retrieve_element', or 'retrieve_elements'. text (str, optional): The text to input (
        only required for 'input_text' action). Defaults to None.

        Returns: Union[bool, List]: Returns True for actions that succeed, and for 'retrieve_element' or
        'retrieve_elements' actions, returns a list of web elements.

        Raises:
            ValueError: If an invalid action is provided.
        """
        try:
            self.selenium.wait_until_element_is_visible(locator)

            actions = {
                'click': lambda: self._click_element(locator),
                'input_text': lambda: self._input_text(locator, text),
                'retrieve_elements': lambda: self._retrieve_elements(locator),
                'retrieve_text': lambda: self._retrieve_text(locator),
            }

            handler = actions.get(action, self._handle_invalid_action)
            return handler()
        except ElementInteractionError as e:
            e.log_error(f"Error interacting with the element: {e}")
            raise ElementInteractionError(f"Error interacting with the element: {e}")
        except Exception as e:
            self.logger.exception(e)
            raise Exception(f"Error occurred while interacting with element: {e}")

    def retrieve_work_item(self, variable: str) -> str:
        """
        Retrieve the work item from the user.

        Args:
            variable (str): Variable name to retrieve.

        Returns:
            str: Retrieved work item.

        Raises:
            KeyError: If the specified variable is not found in the work item variables.
            Exception: If any other unexpected error occurs during retrieval.
        """
        try:
            self.library.get_input_work_item()
            variables = self.library.get_work_item_variables()
            item = variables[variable]
            self.logger.info("Successfully retrieved work item")
            return item
        except KeyError:
            self.logger.exception(f"Variable '{variable}' not found in work item variables")
            raise Exception(f"Variable '{variable}' not found in work item variables")
        except Exception as e:
            self.logger.exception(f"Error retrieving work item: {e}")
            raise Exception(f"Error retrieving work item: {e}")

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

    def __init__(self, selenium: Selenium):
        """
        Initializes GothamistAction with a Selenium instance and URL.
        
        Args:
            selenium (Selenium): Instance of Selenium.
        """
        super().__init__(selenium)

    def _search_variable(self, variable: str) -> None:
        """
        Search for a News phrase on the websites search page.
        This method looks through the gothamist website and inputs the search phrase to search for.
        Upon success, it presses the search button.

        If the elements cannot be retrieved, an exception is raised
        
        Args:
            variable (str): Variable to search.
        """

        try:
            self.logger.info(f"Searching for variable: {variable}")
            self.element_interaction(locator=Selector.SEARCH_INPUT, action='input_text',
                                     text=variable)
            self.element_interaction(locator=Selector.SEARCH_BUTTON, action='click')
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while searching for news phrase: {variable}")
            raise ElementInteractionError(f"Error occurred while searching for news phrase: {e}")

    def _retrieve_description(self) -> list:
        """
        Retrieve the description from the search page.
        This method is used on the search results page, where the various news for the search page is displayed.
        There can be as many as over 100 news articles. We can retrieve their description
        and store it as a list for later use.

        If descriptions for a certain news article are not available, then an empty string is used.
        If the description cannot be located for some reason, an empty list is returned.
        This method does not raise an exception.

        Returns:
            list: List of descriptions.
        """
        try:
            self.logger.info("Retrieving descriptions")
            descriptions = [div.text if div.text is not None else ""
                            for div in self.element_interaction(locator=Selector.DESCRIPTION,
                                                                action='retrieve_elements')]
            return descriptions
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while retrieving descriptions: {e}")
            return []

    def _retrieve_links(self) -> list:
        """
        Retrieve the links from the search page.
        This method is used on the search results page, where the various news for the search page is displayed.
        There can be as many as over 100 news articles. We can retrieve the links for those on the search page.
        Maximum return at once is 10 article links. We can store the links for those on a list for later use.
        If the links cannot be located for some reason, an exception is raised.

        Returns:
            list: List of links.
        """
        try:
            self.logger.info("Retrieving references")
            links = [link.get_attribute("href") for link in
                     self.element_interaction(locator=Selector.LINKS, action='retrieve_elements')]
            self.logger.info("Successfully retrieved references")
            return links
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while retrieving links: {e}")
            raise ElementInteractionError(f"Error occurred while retrieving links: {e}")
        except Exception as e:
            self.logger.exception(f"Error retrieving references: {e}")
            raise Exception(f"Error occurred while retrieving links: {e}")

    def _retrieve_title(self) -> [bool, list]:
        """
        Retrieve the title of the page.
        This method retrieves the title of the news article after the page has navigated to the specific news article
        If the title cannot be located for some reason, an empty string is returned.
        This method does not raise an exception.
        
        Returns:
            str: Title of the page.
        """
        try:
            self.logger.info("Retrieving title")
            title = self.element_interaction(locator=Selector.TITLE, action='retrieve_text')
            self.logger.info('Successfully retrieved title')
            return title
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while retrieving title: {e}")
            return None

    def _retrieve_image(self) -> [bool, list]:
        """
        Retrieve the image from the page.
        This method retrieves the image url for the specific news article after the page
        has navigated to the specific news article. It can be used to download the image or stored as is
        if the image cannot be located for some reason, a None is returned
        This method does not raise an exception.
        
        Returns:
            str: Source URL of the image.
        """
        try:
            self.logger.info("Retrieving image")
            image_source = self.element_interaction(locator=Selector.IMAGE, action='retrieve_elements')[
                0].get_attribute("src")
            image_name = self.element_interaction(locator=Selector.IMAGE_NAME, action='retrieve_text')
            self.logger.info("Successfully retrieved image")
            return image_source, image_name
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while retrieving image: {e}")
            return None
        except Exception as e:
            self.logger.warn(f"Error occurred while retrieving image: {e}")
            return None

    def _retrieve_date(self) -> [bool, list]:
        """
        Retrieve the date from the page.
        This method retrieves the date of the news article after the page has navigated to the specific news article
        It can be used to set a range of date which articles are retrieved, however navigating to specific news article
        is required to utilize this method
        If the date cannot be located for some reason, an empty string is returned.
        This method does not raise an exception.
        
        Returns:
            str: Published date.
        """
        try:
            self.logger.info("Retrieving date")
            date = self.element_interaction(locator=Selector.DATE, action='retrieve_text')
            self.logger.info("Successfully retrieved date")
            return date
        except ElementInteractionError as e:
            e.log_error(f"Error retrieving date: {e}")
            return None

    def _retrieve_news_number(self) -> [bool, list]:
        """
        Retrieve the number of news available for the provided description.
        This method should be used after we have searched for a specific news phrase
        It returns the number of news available for the provided description.
        If the number of news available for the news phrase cannot be located an exception is raised.

        Returns:
            int: Number of news available for the provided description.
        """
        try:
            news_number = self.element_interaction(locator=Selector.NEWS_NUMBER, action='retrieve_text')
            return int(news_number)
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while retrieving news number: {e}")
            raise ElementInteractionError(f"Error occurred while retrieving news number: {e}")
        except Exception as e:
            self.logger.exception(f"Error occurred while retrieving news number: {e}")
            raise Exception(f"Error occurred while retrieving news number: {e}")

    def _handle_links(self, url: Union[str, ParseResult], description: str, search_phrase: str) -> dict:
        """
        Retrieves all the information in the individual news page we want to retrieve and store information from them.
        This method is used to combine all the actions we want to perform on a specific news page.
        It takes in the url, navigates to it, retrieves the title, date, image source and returns all the required data
        for that news in a dictionary format.
        This method does not raise an exception.

        Args:
            url: a link to a specific news page for a specific article.
            description: a description of the article.
            search_phrase: the search phrase used to retrieve the articles.

        Returns:
            dict: dictionary with all the data we retrieved from the link.
        """

        self.browse(url)
        title = self._retrieve_title()
        date = self._retrieve_date()
        image_source, image_name = self._retrieve_image()
        image_dir = download_image(image_source, image_name, Directories.IMAGE_DIRECTORY)
        return {"title": title, "date": date, "description": description,
                "picture_filename": image_dir, "count_phrases_title": count_keyword(title, search_phrase),
                "count_phrases_description": count_keyword(description, search_phrase), 'contains_money_description':
                    check_money(description), 'contains_money_title': check_money(title)}

    def main(self, news_phrase: str) -> list:
        """
        Main function of the script.
        This method is used to combine all the actions we want to perform, all new need to do is enter the news phrase,
        it will open the browser, maximize it to ensure items are visible and search for the news. It will navigate to
        all the news articles required and retrieve all the information.
        The method returns a list of dictionaries containing all the information of the news articles.
        If there is no news or some element causes a problem, it reattempts upto 3 times.
        Upon failure, it raises an exception


        Args:
            news_phrase: the search phrase used to retrieve the articles.

        Returns:
            list: List of dictionaries.
        """
        try:
            self.connect(url=URL.GOTHAMIST_URL)
            self.maximize()
            self._search_variable(news_phrase)
            if self._retrieve_news_number() > 0:
                description = self._retrieve_description()
                links = self._retrieve_links()
                data = []
                for i in range(len(links)):
                    data.append(self._handle_links(url=links[i], description=description[i], search_phrase=news_phrase))
                return data
            else:
                self.logger.warn("No news available")
                self.close_browser()
                return []
        except ElementInteractionError as e:
            e.log_error(f"Error occurred while running the main script: {e}")
            self.close_browser()
            raise ElementInteractionError(f"Error occurred while running the main script: {e}")
        except Exception as e:
            self.logger.exception(f"Error occurred while running the main script: {e}")
            self.close_browser()
            raise Exception(f"Error occurred while running the main script: {e}")
