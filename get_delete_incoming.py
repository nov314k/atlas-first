#!/mingw64/bin/python3

from __future__ import print_function
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


with open("credson/get-delete-incoming.json") as json_file:
    json_data = json.load(json_file)
    scopes = json_data["scopes"]
    tasklists = json_data["tasklists"]
    token_pickle_file = json_data["token_pickle_file"]
    incoming_tasks_file = json_data["incoming_tasks_file"]
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
    print("Filing tasklists...")
    for tl in tasklists:
        tasks = service.tasks().list(tasklist=tl[0]).execute()
        if len(tasks) > 2:
            with open(tl[1], "w") as text_file:
                for t in tasks["items"]:
                    print(t["title"], end='\n', file=text_file)
        else:
            with open(tl[1], "w") as text_file:
                print("There are no tasks in this tasklist.", file=text_file)


def append_tasks():
    with open(tasklists[0][1], "r") as f:
        tasks = f.readlines()
    with open(incoming_tasks_file, "a") as f:
        for t in tasks:
            print(t, end='', file=f)


def delete_tasks(service):
    print("Deleting tasks...")
    tasks = service.tasks().list(tasklist=tasklists[0][0],
                                 showCompleted=True,
                                 showHidden=True).execute()
    if len(tasks) > 2:
        for t in tasks["items"]:
            service.tasks().delete(tasklist=tasklists[0][0], task=t["id"]).execute()


def put_tasks():
    service = get_service()
    file_tasklists(service)
    append_tasks()
    delete_tasks(service)
    print("Reached the end")


if __name__ == "__main__":
    put_tasks()
