import requests
from  gtuparser.util import get_tokens, get_semesters, save_as_json_file,getHeaders, _get_file_data

"""
Http Headers Used:-
__EVENTTARGET: ddlexam --Done
__EVENTARGUMENT: -- Done
__LASTFOCUS: -- Done
__VIEWSTATE -- Done
__VIEWSTATEGENERATOR -- Done
__EVENTVALIDATION -- Done
ddlexam: BE {variable} -- Done
ddlSem: 1 {variable}
ddlBranch: All
LinkButton1: Search 
"""

"""
algorithm
"""

def trigger():
    url = 'http://timetable.gtu.ac.in/'
    
    courses = ['BA', 'BE', 'BH', 'BI', 'BL', 'BP', 'BV', 'DA', 'DI',
              'DP', 'DV', 'FD', 'IC', 'MA', 'MB', 'MC', 'ME', 'MP',
              'PD', 'PP']
    for course in courses:
        r = requests.get(url)
        html = r.text
        r = requests.post(url, getHeaders(html, exam=course))
        semesters = get_semesters(r.text)
        for semester in semesters:
            r = requests.post(url, getHeaders(html,exam = course, sem = semester, submit=True))
            data = _get_file_data(r.text, course, semester)
            save_as_json_file(data)

