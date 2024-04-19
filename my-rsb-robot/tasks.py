from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from script.browser import GothamistAction
from script import utils
from RPA.Browser.Selenium import Selenium


@task
def robot_spare_bin_python():
    get_user_provided_work_item()
    

def get_user_provided_work_item():
    sel = Selenium()
    browser = GothamistAction(sel, url='https://gothamist.com/search')
    browser.connect()
    phrase = browser.retrieve_work_item('news')
    browser.search_variable(phrase)
    refs = browser.retrieve_references()
    description = browser.retrieve_description()
    data = []
    for i in range(len(refs)):
        browser.url = refs[i]
        title = browser.retrive_title()
        image = browser.retrieve_image()
        date = browser.retrieve_date()
        download = utils.download_image(image,'./output/')
        desc_count = utils.count_keyword(description[i], phrase)
        title_count = utils.count_keyword(title,phrase)
        money_desc = utils.check_money(description[i])
        money_title = utils.check_money(title)
        data.append({"title": phrase, "date": date, "description": description[i],
                    "picture_filename": download,"count_phrases_title":title_count, 
            "count_phrases_description":desc_count,'contains_money_description': money_desc,
            'contains_money_title': money_title })
        
    utils.export_data_to_excel(phrase, data)
    browser.close_browser()
    
    

