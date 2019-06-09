#!/mingw64/bin/python3

from __future__ import print_function
import csv
import json
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


with open("credson/write-mensdays.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["scopes"]
    PERIOD = json_data["PERIOD"]
    csv_file = json_data["csv_file"]
    calendar = json_data["calendar"]
    segments = json_data["segments"]
    summaries = json_data["summaries"]
    historical_entry = json_data["historical_entry"]
    historical_dates = json_data["historical_dates"]
    token_pickle_file = json_data["token_pickle_file"]
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


def get_events(service):
    print("Getting existing events...")
    events_result = service.events().list(
        calendarId=calendar, singleEvents=True).execute()
    events = events_result.get("items", [])
    return events


def get_current_first_date(events):
    print("Getting current first date...")
    for event in events:
        if event["summary"] == summaries[0]:
            return event["start"]["date"]


def print_existing_events(events):
    print("Printing existing events...")
    if not events:
        print("No events found")
    else:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            eid = event["id"]
            print(eid, start, event["summary"])


def delete_all_events(service, events):
    print("Deleting all existing events...")
    for event in events:
        service.events().delete(
            calendarId=calendar,
            eventId=event["id"]).execute()


def delete_template_events(service, events):
    print("Deleting all existing template events...")
    for event in events:
        if event["summary"] != historical_entry:
            service.events().delete(
                calendarId=calendar,
                eventId=event["id"]).execute()


def add_new_events(service, new_events):
    print("Adding new events...")
    for ne in new_events:
        event = {
            "summary": ne[0],
            "start": {
                "date": str(ne[1])
            },
            "end": {
                "date": str(ne[1])
            }
        }
        service.events().insert(calendarId=calendar, body=event).execute()
        print("Event created:", ne[1], ne[0])


def write_to_csvfile(datum):
    print("Writing to CSV file...")
    with open(csv_file, newline='') as csvfile:
        existing_rows = []
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            existing_rows.append(row)
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(
            csvfile,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL)
        # Must use square brackets
        csv_writer.writerow(['{:%d-%b-%Y}'.format(datum)])
        for row in existing_rows:
            csv_writer.writerow(row)


def add_historical_events(service, old_dates):
    print("Adding historical events...")
    for od in old_dates:
        event = {
            "summary": historical_entry,
            "start": {
                "date": od
            },
            "end": {
                "date": od
            }
        }
        service.events().insert(calendarId=calendar, body=event).execute()


def write_mensdays():
    day = int(input("First day: "))
    month = int(input("of month : "))
    year = int(input("of year  : "))
    print("Calculation assumes a period of 28 days")
    datum = datetime.date(year, month, day)
    dates_list = [
        datum + datetime.timedelta(days=d)
        for d in range(0, PERIOD + 2)]
    new_events = [
        [summaries[segments[i]], dates_list[i]]
        for i in range(PERIOD + 1)]
    service = authorise_access()
    events = get_events(service)
    # print_existing_events(events)
    current_first_date = get_current_first_date(events)
    if current_first_date:
        add_historical_events(service, [current_first_date])
    delete_template_events(service, events)
    add_new_events(service, new_events)
    write_to_csvfile(datum)


if __name__ == "__main__":
    write_mensdays()
