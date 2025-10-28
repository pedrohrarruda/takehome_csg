from flask import Flask, render_template, jsonify
import requests
import sys
import pandas as pd
import json
from flask_apscheduler import APScheduler

app = Flask(__name__)
users = set()

def requestGitHubAPI(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos").content
    response = json.loads(response)
    return response

def updateDatabase(username, response):
    updated = False
    if username in users:
        updated = True
        df = pd.read_csv('data.csv')
        df = df[df.username != username]
        df.to_csv('data.csv', index=False)
    
    try:
        for item in response[:5]:
            name = item.get('name', 'N/A')
            html_url =  item.get('html_url', 'N/A')
            description = item.get('description', 'N/A')
            if isinstance(description, str):
                description = description.replace(',','')
            language =  item.get('language', 'N/A')
            users.add(username)
            with open('data.csv', 'a') as f:
                f.write(f"{username},{name},{html_url},{description},{language}\n")
    except Exception as e:
            print("User not found")
    return updated


@app.route("/", methods=['GET'])
def home():
    return render_template('indext.html')

@app.route("/<username>", methods=['GET'])
def gitHubRequest(username):
        response = requestGitHubAPI(username)
        updated = updateDatabase(username, response)
        response_envelope = {
        "data": response,
        "message": updated
        }  
        return jsonify(response_envelope)

def my_job():
    for x in users:
        response = requestGitHubAPI(x)
        updateDatabase(x,response)
        print("Updated database", file=sys.stderr)

# Initialize the scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Schedule the job to run every minute
scheduler.add_job(id='job', func=my_job, trigger='interval', minutes=1, misfire_grace_time=60)

