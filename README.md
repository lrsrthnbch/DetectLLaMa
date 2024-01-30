# Malicious Mail LLM Evaluation
 
## Overview
This project automates the process of fetching, evaluating, and displaying emails. It integrates a Python Flask application with a local Large Language Model (LLM) like LLaMA for advanced analysis of emails. This system is designed to identify and evaluate characteristics of emails, such as signs of maliciousness, and display these evaluations through a web interface.

## Features
* Automated Email Fetching: Retrieves new emails for analysis.
* LLM-based Email Evaluation: Utilizes a local LLaMA model for sophisticated natural language understanding to evaluate email content.
* Web Interface: Displays emails and their evaluations, updating in real time.

## Technologies Used
* Python
* Flask
* SQLite
* JavaScript (HTML/CSS)
* Local LLM (e.g., LLaMA)

## LLM Integration for Email Evaluation
The system uses a local instance of the LLaMA model for the evaluation of emails. Here's how it works:

* Fetching Emails: Emails are fetched from a specified source (e.g., an Outlook inbox) using Python scripts.
* Preprocessing: Each email's content is preprocessed and formatted into a query for the LLM.
* LLM Analysis: The LLaMA model analyzes the email content. It is trained to assess various aspects of an email, such as detecting signs of phishing, spam, or other malicious intent.
* Evaluation Results: The model outputs an evaluation score or categorization, which is then stored in a SQLite database along with the email content.

## Setup
Follow these steps to set up and run the project:

1. Clone the Repository:

```
git clone https://github.com/lrsrthnbch/Malicious-Mail-LLM-Evaluation
```
2. Install Dependencies:

```
pip install flask sqlite3 pythoncom win32com.client openai
```

3. Set Up the Database:

```
python database.py
```

## Usage
1. Start the Flask Server:

```
start_webui.bat
```
