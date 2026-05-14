import os
import json
from dotenv import load_dotenv
from ollama import Client
from schemas import CalendarEvent

# Load environment variables
load_dotenv()

# Initialize the Ollama client pointing to the Cloud API
client = Client(
    host='https://ollama.com',
    headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"}
)

def parse_email_to_event(email_text: str) -> CalendarEvent:
    """
    Ingests raw email text and returns a strictly typed CalendarEvent object
    using Ollama Cloud models.
    """
    print("Extracting data from email via Ollama Cloud...\n")
    
    # We pass the Pydantic JSON schema to the format parameter to force structured output
    response = client.chat(
        model="qwen3:480b-cloud", 
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
        format=CalendarEvent.model_json_schema(),
    )
    
    # Ollama returns a JSON string that adheres to our schema.
    # We parse it and unpack it into our Pydantic class.
    parsed_json = json.loads(response['message']['content'])
    return CalendarEvent(**parsed_json)

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