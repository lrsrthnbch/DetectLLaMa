from openai import OpenAI
import os
import json

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def analyze_email(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        email_content = file.read()

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": "You are a highly skilled cybersecurity expert trained in detecting malicious emails. Evaluate the following email for maliciousness. Provide a rating in the format x/10 on how malicious it is. In a new paragraph, write a three sentance summary on why you think that's the case. Be very critical please. Don't consider if the email is polite or not, just look for obvious signs of maliciousness."},
            {"role": "user", "content": email_content}
        ],
        temperature=0.7,
    )

    return completion.choices[0].message.content

def evaluate_emails():
    directory = "mails/"
    results_file = "results/results.txt"

    total_files = len([f for f in os.listdir(directory) if f.endswith(".txt")])
    processed_files = 0

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)

            analysis_result = analyze_email(file_path)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
                sender = content[1].split(": ")[1].strip()
                sender_email = content[2].split(": ")[1].strip()
                subject = content[0].split(": ")[1].strip()

            with open(results_file, 'a', encoding='utf-8') as res_file:
                res_file.write(f"Sender: {sender}\nSender Email: {sender_email}\nSubject: {subject}\n\n")
                res_file.write(f"{analysis_result}\n\n")

            os.remove(file_path)

            processed_files += 1
            print(f"Processed {processed_files} of {total_files} files.")