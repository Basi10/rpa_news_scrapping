import os 
import re
import requests
import uuid
from datetime import datetime
from RPA.Excel.Files import Files
from pathlib import Path





def export_data_to_excel(name, data):
    file_path = '../output/{}.xlsx'.format(name)
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

def download_image(image_url, directory):
    response = requests.get(image_url)
    if response.status_code == 200:
        if not os.path.exists(directory):
            os.makedirs(directory)
        unique_filename = str(uuid.uuid4())
        filename = f"{unique_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        full_path = os.path.join(directory, filename)
        with open(full_path, 'wb') as f:
            f.write(response.content)
        print("Image downloaded and saved successfully:", full_path)
        return full_path
    else:
        print("Failed to download image")
        

def check_money(string):
    money_patterns = [
        r'\$\d+(\.\d+)?',    
        r'\d+\s*(dollars|USD)',   
    ]
    combined_pattern = '|'.join(money_patterns)
    matches = re.findall(combined_pattern, string)
    return bool(matches)


def count_keyword(string, keyword):
    string_lower = string.lower()
    keyword_lower = keyword.lower()
    count = string_lower.count(keyword_lower)
    return count