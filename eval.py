from openai import OpenAI
import sqlite3
import os
import json
import re

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

db_file = 'emails.db'

def analyze_email(email_content):
    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert trained in detecting malicious emails. You provide a very critical and profound opinion if the mail is malicious. You do that by giving it a score from 1-10 (only whole numbers, 10 being the highest maliciousness rating) in the format **X**. Don't deviate from that. After that, you provide a three sentence summary on why it's malicious or not."},
            {"role": "user", "content": email_content}
        ],
        temperature=0.7,
    )

    return completion.choices[0].message.content

def evaluate_emails():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM emails WHERE evaluation IS NULL OR evaluation = ''")
    emails_to_evaluate = cursor.fetchall()

    for email_id, email_content in emails_to_evaluate:
        analysis_result = analyze_email(email_content)

        rating_match = re.search(r'\*\*([1-9]|10)\*\*', analysis_result)
        
        if rating_match:
            rating = rating_match.group(1)
        else:
            rating = None

        cursor.execute("UPDATE emails SET evaluation = ?, rating = ? WHERE id = ?", (analysis_result, rating, email_id))
        conn.commit()

    conn.close()

if __name__ == "__main__":
    evaluate_emails()
