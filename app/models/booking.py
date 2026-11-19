
from datetime import date, time, datetime

from sqlalchemy import String, Date, Time, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)

    candidate_name: Mapped[str] = mapped_column(String(255),nullable=False)

    email: Mapped[str] = mapped_column(String(255),nullable=False)

    interview_date: Mapped[date] = mapped_column(Date,nullable=False)

    interview_time: Mapped[time] = mapped_column(Time,nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
