import azure.functions as func

import fastapi

from dotenv import load_dotenv
import os
from services.jira_service import JiraService
jira_service = JiraService()

load_dotenv()

app = fastapi.FastAPI()

@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }


@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }

@app.get("/start/{name}")
async def start(name: str):
    return {
        "name": name,
    }

@app.get("/issues/{issue_key}")
async def get_jira_issue(issue_key: str):
    try:
        issue = jira_service.get_issue(issue_key)
        return issue
    except Exception as e:
        raise app.HTTPException(status_code=500, detail=str(e))
    
@app.get("/issuess/")
async def search_jira_issues():
    try:
        issues = jira_service.search_issues()
        return issues
    except Exception as e:
        raise app.HTTPException(status_code=500, detail=str(e))