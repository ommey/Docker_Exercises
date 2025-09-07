import os
from flask import Flask, render_template, request

app = Flask(__name__)

# This is a slight improvement from the original by exporting LOG_FILE as dir/file.txt or dir/nameoflog or dir/dir/../name and lastlty or dir/nameoflog or dir/dir/../file.txt 
# first improvement is patching a bug that caused a crash if LOG_FILE="" (empty string).
# second improvement is making it sp that user can choose a directory instead of strictly a txt file.

# Get LOG_FILE from environment, if not set or empty, use "message_log.txt"
LOG_FILE = os.getenv("LOG_FILE") or "message_log.txt"

# If LOG_FILE ends with "/" OR is an existing directory append LOG_FILE a default filename
if LOG_FILE.endswith(os.sep) or os.path.isdir(LOG_FILE):
    LOG_FILE = os.path.join(LOG_FILE, "messages.txt")

# if LOG_FILE doesnt contain a valid location, then create path locally
os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

# Test write to make the log appear during development.
with open(LOG_FILE, 'a') as f:
    f.write("App started\n")

# Test print to make sure log location is correct
print("System logs will be located at: ", LOG_FILE)

# Tells Flask: when a request comes to the root URL /, call index() function. The request may be either GET (normal page load) or POST (form submission)
@app.route('/', methods=['GET', 'POST'])

# Flask will call this function with either a 'GET' or 'POST'
def index():

    # If app.routing caused by 'POST' (submitting data) method
    if request.method == 'POST':

        #read message from the form labeled 'message'
        message = request.form.get('message')

        # write it to LOG_FILE
        with open(LOG_FILE, 'a') as log:
            log.write(message + '\n')

    # If app.routing cause by 'GET' (typically refreshing page) put current messages in a list
    messages = []

    # If LOG_FILE available the create a list populated with the entries separated with '\n'
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            messages = log.read().split('\n')[:-1]

    # Return list data to caller trimmed
    return render_template('index.html',
                            messages=[m.strip() for m in messages],
                            messages_count = len(messages))

# makes sure runner of this app/script hosts to any device on network using port 5000, disabling debug for better Containerizing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=os.getenv("DEBUG", "False") == "TRUE")






