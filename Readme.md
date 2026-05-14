# Smart Inbox Organizer & Calendar Router

## Overview
This project demonstrates how to use Large Language Models (LLMs) in a deterministic, production-ready way using **Structured Outputs**. 

Instead of generating conversational text, this application acts as a middleware parser. It ingests messy, unstructured email data and forces the AI to extract entities (date, time, location, participants) into a strict JSON schema defined by Pydantic.

## The Problem Solved
Traditional AI outputs are non-deterministic strings. If an API expects `{"date": "2023-10-25"}`, and the AI outputs `"Sure! The date is October 25th"`, the application crashes. This project utilizes schema enforcement to guarantee the output matches the exact data types required by downstream services.

## Tech Stack
*   **Python 3.10+**
*   **OpenAI API** (Using the `.parse` method for guaranteed schema adherence)
*   **Pydantic** (For data validation and schema definition)
*   **python-dotenv** (For environment variable management)

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file in the root directory and add your API key:
   `OPENAI_API_KEY=your_api_key_here`

## Usage
Run the main extraction script to see the parser in action:
`python main.py`