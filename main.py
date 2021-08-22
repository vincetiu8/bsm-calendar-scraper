from __future__ import print_function

import datetime
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

switch = input("next monday, is it week a or b? ").lower() == "b"
monday = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=-datetime.datetime.today().weekday(), weeks=1)

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

driver = None
try:
    driver = webdriver.Chrome(executable_path="./chromedriver")
except:
    options = webdriver.ChromeOptions()
    options.binary_location = input("please input the absolute path to your chrome binary: ")
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")

driver.get("https://pupils.britishschoolmanila.org/api/profile/timetable/")
table = None

try:
    table = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
except:
    sys.exit("unable to detect table")

print("loadad timetable")

classes_html = driver.find_elements_by_xpath("//div[contains(@id, 'TTB_PeriodTime_Id_')]")
print("found classes", classes_html)

cal = service.calendars().insert(body={
    "summary": "Subjects",
    "timeZone": "Asia/Manila"
}).execute()

for c in classes_html:
    id_raw = c.get_attribute("id")
    id = int(id_raw.split("_")[-1])
    print("processing class", id)
    id -= 1
    if len(c.find_elements_by_xpath("./..//span[@class='TTB_StudentBoxSubject_Name']")) == 0:
        continue
    teacher = c.find_element_by_xpath("./..//span[@class='TTB_StudentBoxTeacher_Salutation']").text
    day = id // 8
    if switch:
        day = (day + 5) % 10
    if day > 4:
        day += 2
    time = c.text[1:-1].split(" ")
    print(time)
    start = time[0].split(":")
    end = time[-1].split(":")

    event_body = {
        "summary": c.find_element_by_xpath("./..//span[@class='TTB_StudentBoxSubject_Name']").text,
        "description": f"Teacher: {teacher}",
        "start": {
            "dateTime": (monday + datetime.timedelta(days=day, hours=int(start[0]), minutes=int(start[1]))).isoformat(),
            "timeZone": "Asia/Manila"
        },
        "end": {
            "dateTime": (monday + datetime.timedelta(days=day, hours=int(end[0]), minutes=int(end[1]))).isoformat(),
            "timeZone": "Asia/Manila"
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;INTERVAL=2',
        ]
    }

    event = service.events().insert(calendarId=cal["id"], body=event_body).execute()
    print("created event:", event["id"])