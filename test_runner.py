from main import parse_email_to_event
import json

def run_tests():
    test_cases = [
        {
            "name": "Standard Meeting Request",
            "email": "Can we schedule a kick-off call for the new marketing campaign? Let's aim for next Tuesday at 2:00 PM via Google Meet. Please invite marketing@company.com and Sarah."
        },
        {
            "name": "Not an Event (Action Required = False)",
            "email": "Hey everyone, just sharing the attached Q3 financial report for your review. No need to reply. Thanks!"
        },
        {
            "name": "Vague Details (The 'Tomorrow' Problem)",
            "email": "Let's grab lunch tomorrow to discuss the contract. Same place as last time."
        }
    ]

    print("🚀 Running AI Parser Test Suite...\n")
    print("=" * 50)

    for i, test in enumerate(test_cases, 1):
        print(f"TEST {i}: {test['name']}")
        print(f"INPUT: {test['email']}")
        
        try:
            # Call our AI extraction engine
            result = parse_email_to_event(test['email'])
            
            # Print the structured result
            print("\n✅ EXTRACTION SUCCESS:")
            print(result.model_dump_json(indent=2))
        except Exception as e:
            print(f"\n❌ EXTRACTION FAILED: {e}")
            
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    run_tests()