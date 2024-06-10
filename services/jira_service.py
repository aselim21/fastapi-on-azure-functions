import requests
from requests.auth import HTTPBasicAuth
import os
import json

class JiraService:
    def __init__(self):
        self.base_url = os.getenv("CONFLUENCE_BASE_URL")
        self.username = os.getenv("CONFLUENCE_USERNAME")
        self.api_token = os.getenv("CONFLUENCE_API_TOKEN")
        self.jira_route = os.getenv("CONFLUENCE_ROUTE")
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
            
     #https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-post 
    #with the GET version, you can search with less filters
    # This code sample uses the 'requests' library:
    # http://docs.python-requests.org
    def search_issues(self):
        url = f"{self.base_url + self.jira_route}/search/"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        payload = json.dumps( {
        # "expand": [
        #     "names",
        #     "schema",
        #     "operations"
        # ],
        # "fields": [
        #     "summary",
        #     "status",
        #     "assignee"
        # ],
        "fieldsByKeys": False,
        "jql": "project = MYP ORDER BY created DESC",
        "maxResults": 15,
        "startAt": 0
        })

        response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=self.auth
        )

        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))