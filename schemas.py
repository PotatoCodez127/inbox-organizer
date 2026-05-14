from pydantic import BaseModel, Field
from typing import List, Optional

class Participant(BaseModel):
    name: str = Field(description="The full or first name of the participant.")
    email: Optional[str] = Field(default=None, description="The email address, if mentioned. Otherwise null.")

class CalendarEvent(BaseModel):
    action_required: bool = Field(description="True if the email contains a request for a meeting, call, or event.")
    event_title: Optional[str] = Field(default=None, description="A short title for the event. Null if action_required is false.")
    date: Optional[str] = Field(default=None, description="The date in ISO format: YYYY-MM-DD. Null if action_required is false.")
    time: Optional[str] = Field(default=None, description="The start time of the event. Format: HH:MM AM/PM. Null if action_required is false.")
    location: Optional[str] = Field(default=None, description="Physical location or virtual meeting link.")
    participants: List[Participant] = Field(default_factory=list, description="List of all people attending, excluding the email recipient.")