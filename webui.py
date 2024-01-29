from flask import Flask, jsonify, render_template
import logging
import threading
import pythoncom
import os
import time
import fetch
import eval

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def fetch_and_analyze_emails():
    print("Monitoring Outlook for incoming E-Mails...")
    pythoncom.CoInitialize()
    try:
        while True:
            fetch.fetch_emails()
            eval.evaluate_emails()
            time.sleep(10)
    finally:
        pythoncom.CoUninitialize()
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-results', methods=['GET'])
def get_results():
    if os.path.exists('results/results.txt'):
        with open('results/results.txt', 'r') as file:
            results = file.read()
    else:
        results = "No results available yet."
    return jsonify(results)

if __name__ == '__main__':
    threading.Thread(target=fetch_and_analyze_emails, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)