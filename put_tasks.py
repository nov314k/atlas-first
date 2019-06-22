#!/mingw64/bin/python3

from __future__ import print_function
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


with open("settings-private/settings.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["tasks_scopes"]
    tasklists = json_data["tasklists"]
    token_pickle_file = json_data["tasks_token_pickle_file"]
    todays_tasks_file = json_data["directory"] + json_data["today"]
    credentials_json_file = json_data["tasks_credentials_json_file"]


def get_service():
    print("Getting service...")
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
    service = build("tasks", "v1", credentials=creds)
    return service


def file_tasklists(service):
    print("Filing tasklists...")
    for tl in tasklists:
        tasks = service.tasks().list(tasklist=tl[0]).execute()
        if len(tasks) > 2:
            with open(tl[1], "w") as text_file:
                for t in tasks["items"]:
                    print(t["title"], end='', file=text_file)
        else:
            with open(tl[1], "w") as text_file:
                print("There are no tasks in this tasklist.", file=text_file)


def upload_tasks(service):
    print("Uploading tasks...")
    with open(todays_tasks_file, "r") as text_file:
        tasks = text_file.readlines()
    for t in tasks[::-1]:
        if len(t) > 1:
            task = {
                "title": t
            }
            service.tasks().insert(tasklist='@default', body=task).execute()


def delete_tasks(service):
    print("Deleting tasks...")
    tasks = service.tasks().list(tasklist="@default",
                                 maxResults=100,
                                 showCompleted=True,
                                 showHidden=True).execute()
    if len(tasks) > 2:
        if len(tasks) > 3:
            next_page_token = tasks["nextPageToken"]
        else:
            next_page_token = False
        for t in tasks["items"]:
            service.tasks().delete(tasklist="@default", task=t["id"]).execute()
        while next_page_token:
            tasks = service.tasks().list(tasklist="@default",
                                         maxResults=100,
                                         showCompleted=True,
                                         pageToken=next_page_token,
                                         showHidden=True).execute()
            if len(tasks) > 2:
                for t in tasks["items"]:
                    service.tasks().delete(tasklist="@default",
                                           task=t["id"]).execute()


def put_tasks():
    service = get_service()
    # file_tasklists(service)
    delete_tasks(service)
    upload_tasks(service)
    print("~~~ THE END ~~~")


if __name__ == "__main__":
    put_tasks()
