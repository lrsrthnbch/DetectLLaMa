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
        return True  # Return True to indicate that a new email was saved
    return False  # No new email was saved

def fetch_emails():
    new_emails_fetched = False  # Track whether any new emails were fetched
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)
    emails = inbox.Items.Restrict("[UnRead] = True")  # Filter for only unread emails

    for email in emails:
        if save_email_content(email):
            new_emails_fetched = True
            email.UnRead = False  # Mark as read only after successful save

    return new_emails_fetched  # Return whether any new emails were fetched

if __name__ == "__main__":
    fetch_emails()
