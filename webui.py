from flask import Flask, jsonify, render_template
import sqlite3
import logging
import threading
import pythoncom
import os
import time
import fetch
import eval

app = Flask(__name__)

db_file = 'emails.db'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def fetch_and_analyze_emails():
    print("Monitoring Outlook for incoming E-Mails...")
    while True:
        pythoncom.CoInitialize()

        new_emails_fetched = fetch.fetch_emails()

        if new_emails_fetched:
            eval.evaluate_emails()

        pythoncom.CoUninitialize()

        time.sleep(3)


@app.route('/get-results', methods=['GET'])
def get_results():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    emails = cursor.fetchall()
    conn.close()
    email_list = []
    for email in emails:
        email_dict = {
            "id": email[0],
            "subject": email[1],
            "sender": email[2],
            "sender_address": email[3],
            "timestamp": email[4],
            "content": email[5],
            "evaluation": email[6],
            "rating": email[7]
        }
        email_list.append(email_dict)
    return jsonify(email_list)

@app.route('/get-log', methods=['GET'])
def get_log():
    try:
        with open('C:\\tmp\\lmstudio-server-log.txt', 'r', encoding='utf-8') as file:
            log_data = file.readlines()[-100:]
        return ''.join(log_data), 200, {'Content-Type': 'text/plain'}
    except UnicodeDecodeError:
        return "Error reading log file", 500

@app.route('/reset-database', methods=['POST'])
def reset_database():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emails")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='emails'")
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Database reset successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/')
def index():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    emails = cursor.fetchall()
    conn.close()
    return render_template('index.html', emails=emails)

if __name__ == '__main__':
    threading.Thread(target=fetch_and_analyze_emails, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)