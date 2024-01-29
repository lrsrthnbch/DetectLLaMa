import win32com.client
import os
import datetime

def save_email_content(email, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Subject: {email.Subject}\n")
        file.write(f"Sender: {email.SenderName}\n")
        file.write(f"Sender Email: {email.SenderEmailAddress}\n")
        file.write(f"Received Time: {email.ReceivedTime}\n")
        file.write(f"Body:\n{email.Body}\n")

def fetch_emails():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    save_path = "mails/"

    for email in inbox.Items:
        if email.UnRead:
            email.UnRead = False

            filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{email.SenderName}.txt"
            filepath = os.path.join(save_path, filename)

            save_email_content(email, filepath)