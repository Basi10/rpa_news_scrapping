import os
import re
import requests
import logging
import robocorp.log as logging
from RPA.Excel.Files import Files
from pathlib import Path
from script.constants import (
     Directories
)


def export_data_to_excel(name, data):
    """
    Export data to an Excel file.

    Args:
        name (str): Name of the Excel file.
        data (list): List of dictionaries representing rows of data.

    Returns:
        None
    """
    if not name.endswith(Directories.EXCEL_FILE_EXT):
        name += Directories.EXCEL_FILE_EXT

    file_path = os.path.join(Directories.EXCEL_DIRECTORY, name)
    excel = Files()
    if Path(file_path).is_file():
        excel.open_workbook(file_path)
        if name in excel.list_worksheets():
            excel.append_rows_to_worksheet(content=data)
            excel.save_workbook()
    else:
        excel.create_workbook(name)
        excel.create_worksheet(name=name, content=data, header=True)
        excel.save_workbook(file_path)
    logging.info(f"Data exported to Excel file: {file_path}")


def download_image(image_url, image_name, directory):
    """
    Download an image from a URL and save it to a directory.

    Args:
        image_url (str): URL of the image.
        image_name (str): Name of the image file.
        directory (str): Directory to save the image.

    Returns:
        str: Full path to the downloaded image file, or None if download failed.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        if not os.path.exists(directory):
            os.makedirs(directory)    
        full_path = os.path.join(directory, "{}.jpg".format(image_name.replace('/', '')))
        with open(full_path, 'wb') as f:
            f.write(response.content)
        print("Image downloaded and saved successfully:", full_path)
        return full_path
    else:
        print("Failed to download image")
        return None


def check_money(string):
    """
    Check if string contains money values or not.

    Args:
        string (str): Input string.

    Returns:
        bool: True if string contains money values, False otherwise.
    """
    money_patterns = [
        r'\$\d+(\.\d+)?',
        r'\d+\s*(dollars|USD)',
    ]
    combined_pattern = '|'.join(money_patterns)
    matches = re.findall(combined_pattern, string)
    return bool(matches)


def count_keyword(string, keyword):
    """
    Count the number of occurrences of a keyword within a string.

    Args:
        string (str): Input string.
        keyword (str): Keyword to search for.

    Returns:
        int: Number of occurrences of the keyword in the string.
    """
    string_lower = string.lower()
    keyword_lower = keyword.lower()
    count = string_lower.count(keyword_lower)
    return count
