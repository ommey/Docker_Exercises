import os
from flask import Flask, render_template, request

app = Flask(__name__)

# This is a simple way to check whether user has
# 
LOG_FILE = os.getenv("LOG_FILE") or "message_log.txt"

# Ensure the directory exists if LOG_FILE has a path
if os.path.dirname(LOG_FILE):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


print("LOG_FILE is:", LOG_FILE)




