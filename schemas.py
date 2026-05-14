from pydantic import BaseModel, Field
from typing import List, Optional

class Participant(BaseModel):
    name: str = Field(description="The full or first name of the participant.")
    email: Optional[str] = Field(description="The email address, if mentioned. Otherwise null.")

class CalendarEvent(BaseModel):
    action_required: bool = Field(description="True if the email contains a request for a meeting, call, or event.")
    event_title: str = Field(description="A short, professional title for the calendar event.")
    date: str = Field(description="The date of the event in ISO format: YYYY-MM-DD. Infer the year based on context if missing.")
    time: str = Field(description="The start time of the event. Format: HH:MM AM/PM")
    location: Optional[str] = Field(description="Physical location or virtual meeting link.")
    participants: List[Participant] = Field(description="List of all people attending, excluding the email recipient.")