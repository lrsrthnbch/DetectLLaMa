from openai import OpenAI
import sys
import time

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def analyze_email(email_content):
    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": "Your task is to evaluate the following Email for maliciousness. If the Email is malicious reply with: flagged as malicious. If the Email is safe reply with: flagged as safe."},
            {"role": "user", "content": email_content}
        ],
        temperature=0.6,
    )
    return completion.choices[0].message.content

def read_email_content(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

phishing_files = [f"p{i}.txt" for i in range(1, 6)]
safe_files = [f"s{i}.txt" for i in range(1, 6)]
email_files = phishing_files + safe_files

evaluations_per_email = 10 

def evaluate_emails(email_files, evaluations_per_email):
    open('other_responses.txt', 'w').close()
    
    for file_name in email_files:
        email_content = read_email_content(file_name)
        phishing_count = 0
        safe_count = 0
        other_responses_count = 0
        
        print(f"Evaluating {file_name}...")
        
        for i in range(evaluations_per_email):
            response = analyze_email(email_content).strip()
            normalized_response = response.lower().rstrip('.')
            
            if normalized_response == "flagged as malicious":
                phishing_count += 1
            elif normalized_response == "flagged as safe":
                safe_count += 1
            else:
                other_responses_count += 1
                with open('other_responses.txt', 'a') as response_file:
                    response_file.write(f"{file_name} {i+1}: {response}\n")
            
            print(f"\r{i+1}/{evaluations_per_email}", end='', flush=True)
        
        print(f"\nResults for {file_name}:")
        print(f"Phishing attempt detected: {phishing_count} times")
        print(f"Emails marked as safe: {safe_count} times")
        print(f"Other responses: {other_responses_count} times")

start_time = time.time()
evaluate_emails(email_files, evaluations_per_email)
end_time = time.time()

execution_time = end_time - start_time
print(f"Total execution time: {execution_time:.2f} seconds")