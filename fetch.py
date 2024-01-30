import sqlite3
import win32com.client
import os
import datetime

db_file = 'emails.db'

def email_exists(subject, sender, timestamp):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM emails WHERE subject = ? AND sender = ? AND timestamp = ?", (subject, sender, timestamp))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_email_content(email):
    subject = email.Subject
    sender = email.SenderName
    sender_address = email.SenderEmailAddress
    timestamp = email.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S")
    content = email.Body

    if not email_exists(subject, sender, timestamp):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emails (subject, sender, sender_address, timestamp, content) VALUES (?, ?, ?, ?, ?)", (subject, sender, sender_address, timestamp, content))
        conn.commit()
        conn.close()

def fetch_emails():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    for email in inbox.Items:
        if email.UnRead:
            email.UnRead = False
            save_email_content(email)

if __name__ == "__main__":
    fetch_emails()

# fetch_emails()