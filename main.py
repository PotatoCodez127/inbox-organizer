import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schemas import CalendarEvent

# Load environment variables
load_dotenv()

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_email_to_event(email_text: str) -> CalendarEvent:
    """
    Ingests raw email text and returns a strictly typed CalendarEvent object.
    """
    print("Extracting data from email...\n")
    
    # We use the .parse method which guarantees the output matches our Pydantic model
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini", # A fast, cost-effective model for data extraction
        messages=[
            {
                "role": "system", 
                "content": "You are a precise data extraction algorithm. Extract calendar event details from the provided email. If the email does not contain a meeting request, set action_required to false."
            },
            {
                "role": "user", 
                "content": email_text
            }
        ],
        response_format=CalendarEvent,
    )
    
    # Return the parsed Pydantic object
    return response.choices[0].message.parsed

if __name__ == "__main__":
    # Mock Email Data
    raw_email = """
    Hey team,
    Just wanted to sync up on the Q3 roadmap. Let's grab coffee next Thursday at 10:30 AM at the Starbucks on Main Street. 
    Sarah and John (john.doe@example.com) will be joining us. 
    Let me know if that works!
    - Alex
    """
    
    print(f"RAW EMAIL:\n{raw_email}\n")
    print("-" * 40)
    
    # Execute extraction
    extracted_event = parse_email_to_event(raw_email)
    
    # Output the result as JSON
    print("\nSTRUCTURED JSON OUTPUT:")
    print(extracted_event.model_dump_json(indent=2))