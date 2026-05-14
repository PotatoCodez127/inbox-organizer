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
        model="gemma4:31b-cloud", 
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are a precise data extraction algorithm. Extract calendar event details "
                    "from the provided email into a flat JSON object. "
                    "CRITICAL INSTRUCTIONS: "
                    "1. If the email does not contain a meeting request, set action_required to false and leave other fields null. "
                    "2. Do NOT nest the output inside an 'event_details' key. Use the exact keys provided in the schema at the root level."
                )
            },
            {
                "role": "user", 
                "content": email_text
            }
        ],
        format=CalendarEvent.model_json_schema(),
    )
    
    # 1. Capture the raw text output
    raw_content = response['message']['content'].strip()
    
    # 2. Check for empty responses (often caused by auth errors or API timeouts)
    if not raw_content:
        raise ValueError("The model returned an empty response. Double-check your API key in .env.")
        
    # 3. Sanitize the output: Strip markdown code blocks if the model included them
    if raw_content.startswith("```json"):
        raw_content = raw_content[7:] # Remove ```json
    elif raw_content.startswith("```"):
        raw_content = raw_content[3:] # Remove generic ```
        
    if raw_content.endswith("```"):
        raw_content = raw_content[:-3] # Remove trailing ```
        
    raw_content = raw_content.strip() # Clean up any lingering whitespace
    
    # 4. Safely attempt to parse
    try:
        parsed_json = json.loads(raw_content)
        return CalendarEvent(**parsed_json)
    except json.JSONDecodeError as e:
        # If it STILL fails, print exactly what the model gave us so we can debug
        print(f"\n[DEBUG] RAW MODEL OUTPUT THAT FAILED TO PARSE:\n{raw_content}\n")
        raise e

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