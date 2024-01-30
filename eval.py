from openai import OpenAI
import sqlite3
import os
import json

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

db_file = 'emails.db'

def analyze_email(email_content):
    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": "You are a highly skilled cybersecurity expert trained in detecting malicious emails. Evaluate the following email for maliciousness. Provide a rating in the format x/10 on how malicious it is. In a new paragraph, write a three sentence summary on why you think that's the case. Be very critical please. Don't consider if the email is polite or not, just look for obvious signs of maliciousness."},
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

        cursor.execute("UPDATE emails SET evaluation = ? WHERE id = ?", (analysis_result, email_id))
        conn.commit()

    conn.close()

if __name__ == "__main__":
    evaluate_emails()

# evaluate_emails()