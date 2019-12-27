# Contains utility of module
# <select.*?name="(.*?)".*?>.*?\n+(?:.*?<option.*?>(.*?)<\/option>.*?\n)+\n?<\/select>
# (?:\G(?!\A)|\bid='Gender'>)\s*<option\s[^<]*?value='(?<val>\‌​d+)'>(?<txt>[^<]*)</‌​option>
# final   : <select.*?name="(.*?)".*?>((\s+.*?\s+)+)<\/select>
# final 2 : <select.*?name="(.*?)".*?>((?:\s+.*?\s+)+)<\/select>
# final 3 : <select.*?name="ddlSem".*?>((?:\s+.*?\s+)+)<\/select>
# Option Setting:
# 	<option.*?value="(.*?)".*?>([^<]+)
# Regex for Inputs
# final <input.*?name="(.*?)".*?value="(.*?)"
# Table Data Needed:-
# id = grddata

#File Data
# table :- <table.*?id="grddata".*?>((?:\s+.*?\s+)+)</tbody>
# rows :- <tr.*?>\s+<td>\s+([^<]+)</td><td>\s+<span.*?>([^<]+)</span>\s+</td><td>\s+([^<]+)
import re
import requests
import csv

def get_semesters(html):
    # Used to get Options from object
    res = re.compile('<select.*?name="ddlSem".*?>((?:\s+.*?\s+)+)<\/select>')
    tokens =_get_options(res.findall(html))
    return tokens[0]


def get_tokens(html):
    # Used to Name and Value Object
    res = re.findall('<input.*?name="(.*?)".*?value="(.*?)"', html)
    _storage = {}
    for result in res:
        _storage[result[0]] = result[1]
    return _storage


def save_as_json_file(data):
    # Used to save Json File
    with open('data.csv','a') as file:
        csv_out = csv.writer(file)
        csv_out.writerow(['course','data','name'])
        for row in data:
            csv_out.writerow(row)


def _get_options(options):
    # This will return options
    res = re.compile('<option.*?value="(.*?)".*?>[^<]+')
    _storage = []
    for option in options:
        _storage.append(res.findall(option))
    return _storage


def _get_file_data(data, course, sem):
    reg = re.compile(
        '<tr.*?bgcolor="(?:#F7F6F3|White)">\s+<td>.*\s+([0-9]{2})\s+.*\s+<span.*?>([^<]+).*\s+.*\s+(.*)')
    _storage = reg.findall(data)
    if _storage == []:
        print("Error", course , sem)
    return _storage


def getHeaders( html, exam="", sem=None, submit = False ):
    """Returns Appropriate Headers for current website
    
    Args:
        html (str): Html of Current Subsiquent
        exam (str, optional): Exam type
        sem (None, optional): Semester, Current one
        submit (bool, optional): if it Submit or not
    
    Returns:
        dict: Returns Headers
    """
    tokens = get_tokens(html)
    headers = {
        "__EVENTTARGET" : "",
        "__EVENTARGUMENT" : "",
        "__LASTFOCUS" : "",
        "ddlexam" : exam,
        "ddlSem" : 1 if sem is None else sem,
        "ddlBranch" : "All",
        "LinkButton1" : "Search"
    }
    for token in tokens.items():
        headers[token[0]] = token[1]

    if not submit:
        headers.pop('LinkButton1')
        headers['ddlSem'] = 1
        headers['__EVENTTARGET'] = "ddlexam"
    return headers
