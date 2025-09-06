import os
from flask import Flask, render_template, request

app = Flask(__name__)

# This is a slight improvement from the original by exporting LOG_FILE as dir/file.txt or dir/nameoflog or dir/dir/../name and lastlty or dir/nameoflog or dir/dir/../file.txt 
# first improvement is patching a bug that caused a crash if LOG_FILE="" (empty string).
# second improvement is making it sp that user can choose a directory instead of strictly a txt file.

# Get LOG_FILE from environment, default to "message_log.txt" in current dir
LOG_FILE = os.getenv("LOG_FILE") or "message_log.txt"

# If LOG_FILE ends with "/" OR is an existing directory → append a default filename
if LOG_FILE.endswith(os.sep) or os.path.isdir(LOG_FILE):
    LOG_FILE = os.path.join(LOG_FILE, "messages.txt")

# Ensure the parent directory exists (if any)
os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

# Test write (optional, can be removed later)
with open(LOG_FILE, 'a') as f:
    f.write("App started\n")


print("System logs will be located at: ", LOG_FILE)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')

        with open(LOG_FILE, 'a') as log:
            log.write(message + '\n')

    messages = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'a') as log:
            messages = log.read().split('\n')[:-1]

    return render_template('index.html', messages=[m.strip() for m in messages])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=os.getenv("DEBUG", "False") == "TRUE")






