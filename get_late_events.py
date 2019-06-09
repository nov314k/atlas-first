#!/mingw64/bin/python3

from __future__ import print_function
import sys
import json
import pickle
import codecs
import os.path
import datetime
from transliterate import transliterate
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


with open("credson/get-late-events.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["scopes"]
    calendars = json_data["calendars"]
    token_pickle_file = json_data["token_pickle_file"]
    late_events_file = json_data["late_events_file"]
    credentials_json_file = json_data["credentials_json_file"]


def authorise_access():
    print("Authorising access...")
    creds = None
    if os.path.exists(token_pickle_file):
        with open(token_pickle_file, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json_file, scopes)
            creds = flow.run_local_server()
        with open(token_pickle_file, "wb") as token:
            pickle.dump(creds, token)
    service = build("calendar", "v3", credentials=creds)
    return service


def get_existing_events(service, calendar, fromDate, toDate):
    print("Getting existing events... from calendar", calendar)
    events_result = service.events().list(
        calendarId=calendar,
        timeMin=fromDate,
        timeMax=toDate,
        singleEvents=True).execute()
    events = events_result.get("items", [])
    return events


def file_existing_events(events, tag):
    print("Filing existing events... to", late_events_file)
    with open(late_events_file, "a") as text_file:
        for event in events:
            print(event["start"]["date"],
                  transliterate(event["summary"]),
                  tag,
                  file=text_file)


def gen_late_events_file(service, from_date, to_date):
    with open(late_events_file, "w") as text_file:
        print("1971-01-01 Start of Unix Epoch +calUnix", file=text_file)
    fromDate = "{:%Y-%m-%d}".format(from_date) + "T00:00:00Z"
    toDate = "{:%Y-%m-%d}".format(to_date) + "T23:59:59Z"
    for c in calendars:
        events = get_existing_events(service, c[1], fromDate, toDate)
        file_existing_events(events, c[0])


def get_late_events():
    print("---------------")
    print("GET LATE EVENTS")
    print("---------------")
    from_day = int(input("From day  : "))
    from_month = int(input("From month: "))
    from_year = int(input("From year : "))
    to_day = int(input("To day    : "))
    to_month = int(input("To month  : "))
    to_year = int(input("To year   : "))
    from_date = datetime.date(from_year, from_month, from_day)
    to_date = datetime.date(to_year, to_month, to_day)
    service = authorise_access()
    gen_late_events_file(service, from_date, to_date)
    print("Reached the end")


if __name__ == "__main__":
    get_late_events()
