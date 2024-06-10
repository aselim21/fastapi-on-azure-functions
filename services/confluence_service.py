import requests
from requests.auth import HTTPBasicAuth
import os
import json

class JiraService:
    def __init__(self):
        self.base_url = os.getenv("JIRA_BASE_URL")
        self.username = os.getenv("JIRA_USERNAME")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.jira_route = os.getenv("JIRA_ROUTE")
        self.auth = HTTPBasicAuth(self.username, self.api_token)

    def get_issue(self, issue_key):
        url = f"{self.base_url + self.jira_route}/issue/{issue_key}"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.raise_for_status())

    def create_issue(self, project_key, summary, issue_type, description):
        url = f"{self.base_url + self.jira_route}/issue"
        payload = {
            "fields": {
                "project": {
                    "key": project_key
                },
                "summary": summary,
                "issuetype": {
                    "name": issue_type
                },
                "description": description
            }
        }
        response = requests.post(url, json=payload, auth=self.auth)
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()