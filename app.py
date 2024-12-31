from flask import Flask, request
from linkedin_api import Linkedin
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

api = Linkedin("VITE_EMAIL", "VITE_PASSWORD")

@app.route("/save", methods=["POST"])
def save_data():
    username = request.json 
    user = api.get_profile(username)
    # if username is not valid
    if user == {}:
        return {"error" : False, "isValid" : False}
    # if username is valid
    else:
        userNetwork = api.get_profile_network_info(username)
        all_skills = api.get_profile_skills(username)
        
        name = f"{user['firstName']} {user['lastName']}"
        bio = user["summary"]
        headline = user["headline"]
        connections = userNetwork["connectionsCount"]
        followers = userNetwork["followersCount"]
        skills = ", ".join(skill["name"] for skill in all_skills)
        data = {
            "name" : name,
            "bio" : bio,
            "headline" : headline,
            "connections" : connections,
            "followers" : followers,
            "skills" : skills,
            "error" : False,
            "isValid" : True
        }
        return data
        
@app.route("/")
def home():
    return "Server is running"
