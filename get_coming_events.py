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


with open("credson/get-coming-events.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["scopes"]
    calendars = json_data["calendars"]
    token_pickle_file = json_data["token_pickle_file"]
    coming_events_file = json_data["coming_events_file"]
    credentials_json_file = json_data["credentials_json_file"]
    all_calendars_dump_file = json_data["all_calendars_dump_file"]


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
    print("Filing existing events... to", all_calendars_dump_file)
    with open(all_calendars_dump_file, "a") as text_file:
        for event in events:
            print(event["start"]["date"],
                  transliterate(event["summary"]),
                  tag,
                  file=text_file)


def gen_calendars_dump_file(service, reference_day, days_before, days_after):
    with open(all_calendars_dump_file, "w") as text_file:
        print("1971-01-01 Start of Unix Epoch +calUnix", file=text_file)
    fromDate = "{:%Y-%m-%d}".format(
        reference_day - datetime.timedelta(days=days_before)) + "T00:00:00Z"
    toDate = "{:%Y-%m-%d}".format(
        reference_day + datetime.timedelta(days=days_after)) + "T23:59:59Z"
    for c in calendars:
        events = get_existing_events(service, c[1], fromDate, toDate)
        file_existing_events(events, c[0])


def gen_coming_events_file(reference_day, days_lookahead):
    print("Writing lookahead file... to", coming_events_file)
    with open(all_calendars_dump_file, "r") as text_file:
        calevs = text_file.readlines()
    calevs.sort()
    interested_in_dates = [
        "{:%Y-%m-%d}".format(reference_day + datetime.timedelta(days=d))
        for d in range(0, days_lookahead + 1)]
    with open(coming_events_file, "w") as text_file:
        for e in calevs:
            if e[0:10] in interested_in_dates:
                print(e, file=text_file, end='')


def get_coming_events(year, month, day):
    print("-----------------------------")
    print("GET TODAY'S AND COMING EVENTS")
    print("-----------------------------")
    # day = int(input("Reference day  : "))
    # month = int(input("Reference month: "))
    # year = int(input("Reference year : "))
    # days_lookahead = int(input("Lookahead days : "))
    days_lookahead = 2
    # TODO Why can't this be = days_lookahead (for the same period)?
    days_after = days_lookahead - 1
    # TODO Why can't this be = 0 (for current day)?
    days_before = 1
    reference_day = datetime.date(year, month, day)
    service = authorise_access()
    gen_calendars_dump_file(service, reference_day, days_before, days_after)
    gen_coming_events_file(reference_day, days_lookahead)
    print("Reached the end")


if __name__ == "__main__":
    get_coming_events()
