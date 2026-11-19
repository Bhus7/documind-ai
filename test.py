from app.db.database import SessionLocal
from app.services.booking import save_interview_booking

details = {
    "candidate_name": "John Smith",
    "email": "john@example.com",
    "interview_date": "2026-11-25",
    "interview_time": "10:30"
}

db = SessionLocal()

try:
    booking = save_interview_booking(db, details)

    print("Booking saved successfully!")
    print("Booking ID:", booking.id)
    print("Candidate:", booking.candidate_name)

finally:
    db.close()