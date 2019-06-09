#!/mingw64/bin/python3

from __future__ import print_function
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


with open("credson/get-tasks.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["scopes"]
    tasklists = json_data["tasklists"]
    token_pickle_file = json_data["token_pickle_file"]
    credentials_json_file = json_data["credentials_json_file"]


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
    for tl in tasklists:
        tasks = service.tasks().list(tasklist=tl[0]).execute()
        if len(tasks) > 2:
            with open(tl[1], "w") as text_file:
                for t in tasks["items"]:
                    print(t["title"], end='', file=text_file)
        else:
            with open(tl[1], "w") as text_file:
                print("There are no tasks in this tasklist.", end='', file=text_file)


def get_tasks():
    service = get_service()
    file_tasklists(service)


if __name__ == "__main__":
    get_tasks()
