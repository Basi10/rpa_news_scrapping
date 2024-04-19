import os 
import re
import requests
import subprocess
import uuid
from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from RPA.Browser.Selenium import Selenium, By
from RPA import Browser
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Excel.Files import Files
from pathlib import Path


@task
def robot_spare_bin_python():
    get_user_provided_work_item()
    

def get_user_provided_work_item():
    lib = Selenium()
    lib.set_selenium_timeout(1000)
    library = WorkItems()
    library.get_input_work_item()
    variables = library.get_work_item_variables()
    news = variables['news']
    print(variables['months'])
    lib.open_available_browser("https://gothamist.com/search")
    lib.go_to("https://gothamist.com/search")
    lib.maximize_browser_window()
    lib.wait_until_element_is_visible("class:search-page-input", timeout=1000)
    lib.input_text_when_element_is_visible("class:search-page-input", news)
    lib.click_element('class:search-page-button')
    lib.wait_until_element_is_visible('class:h2')
    s = lib.find_elements('class:card-title-link')
    refs = []
    description = []
    data = []
    for div in s:
        h = div.get_attribute("href")
        #print(h)
        refs.append(h)
    # This is the method that we get the description from 
    desc = lib.find_elements('class:card-slot')
    for divi in desc:
        i = divi.text
        #print(i)
        description.append(i)
    for i in range(len(refs)):
        lib.go_to(refs[i])
        n = lib.get_text('class:h2')
        print(n)
        lib.wait_until_element_is_visible('class:image-with-caption-wrapper')
        img = lib.find_element('class:image-with-caption-wrapper')
        image_element = img.find_element(by=By.CLASS_NAME,value='image')
        image_source = image_element.get_attribute("src")
        print(image_source)
        d = lib.get_text('class:date-published')
        print(d)
        download = download_image(image_source,'./output/')
        desc_count = description[i].lower().count(news.lower())
        title_count = n.lower().count(news.lower())
        print(desc_count)
        print(title_count)
        money_desc = check_money(description[i])
        money_title = check_money(n)
        data.append({"title": n, "date": d, "description": description[i], "picture_filename": 
            download,"count_phrases_title":title_count, "count_phrases_description": desc_count,
            'contains_money_description': money_desc,'contains_money_title': money_title })
        
    export_data_to_excel(news, data)
    lib.close_browser()
    
    

def export_data_to_excel(name, data):
    # Initialize the Excel Files library
    file_path = './output/{}.xlsx'.format(name)
    excel = Files()
    if Path(file_path).is_file():
        excel.open_workbook(file_path)
        if name in excel.list_worksheets():
            excel.append_rows_to_worksheet(content=data)
            excel.save_workbook()
    else:
        excel.create_workbook(name)    
        excel.create_worksheet(name=name,content=data,header=True)
        excel.save_workbook(file_path)

# Function to download and save the image
def download_image(image_url, directory):
    # Send an HTTP request to the image URL
    response = requests.get(image_url)
    if response.status_code == 200:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Combine directory and filename to create the full path
        unique_filename = str(uuid.uuid4())
        filename = f"{unique_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        full_path = os.path.join(directory, filename)
        # Open the file in binary write mode and write the image content
        with open(full_path, 'wb') as f:
            f.write(response.content)
        print("Image downloaded and saved successfully:", full_path)
        return full_path
    else:
        print("Failed to download image")
        

def check_money(string):
    # Define regular expressions for matching different money formats
    money_patterns = [
        r'\$\d+(\.\d+)?',    
        r'\d+\s*(dollars|USD)',   
    ]
    combined_pattern = '|'.join(money_patterns)
    matches = re.findall(combined_pattern, string)
    return bool(matches)