
import json
from datetime import date
from sqlalchemy.orm import Session
from app.models.booking import InterviewBooking
import ollama


def extract_booking_details(
    messages: list[dict[str, str]]
) -> dict:

    today = date.today().isoformat()

    system_prompt = f"""
    You are an interview booking information extractor.

    Today's date is {today}.

    Read the conversation and extract these fields:

    1. booking_intent
    2. candidate_name
    3. email
    4. interview_date
    5. interview_time
    6. user_confirmed

    Rules:
    - Do not invent missing information.
    - Use null for information not provided.
    - Return interview_date in YYYY-MM-DD format.
    - Return interview_time in 24-hour HH:MM format.
    - Convert relative dates using today's date.
    - user_confirmed must be true only when the user
      explicitly confirms the final booking details.
    - Return valid JSON only.

    Expected JSON structure:

    {{
        "booking_intent": false,
        "candidate_name": null,
        "email": null,
        "interview_date": null,
        "interview_time": null,
        "user_confirmed": false
    }}
    """

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ],
        format="json"
    )

    extracted_data = json.loads(
        response["message"]["content"]
    )

    return extracted_data


def get_missing_booking_fields(details: dict) -> list[str]:

    required_fields = [
        "candidate_name",
        "email",
        "interview_date",
        "interview_time"
    ]

    missing_fields = []

    for field in required_fields:
        if not details.get(field):
            missing_fields.append(field)

    return missing_fields

def get_next_booking_question(missing_fields: list[str]) -> str:

    questions = {
        "candidate_name": "May I have your full name?",
        "email": "What is your email address?",
        "interview_date": "What date would you prefer for the interview?",
        "interview_time": "What time would you prefer for the interview?"
    }

    if missing_fields:
        next_field = missing_fields[0]
        return questions[next_field]

    return (
        "I have collected all your booking details. "
        "Would you like me to confirm this interview booking?"
    )


def create_booking_confirmation(details: dict) -> str:

    return (
        "Please review your interview booking details:\n\n"
        f"Name: {details['candidate_name']}\n"
        f"Email: {details['email']}\n"
        f"Date: {details['interview_date']}\n"
        f"Time: {details['interview_time']}\n\n"
        "Would you like me to confirm this booking?"
    )


def save_interview_booking(
    db: Session,
    details: dict
) -> InterviewBooking:

    booking = InterviewBooking(
        candidate_name=details["candidate_name"],
        email=details["email"],
        interview_date=details["interview_date"],
        interview_time=details["interview_time"]
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking