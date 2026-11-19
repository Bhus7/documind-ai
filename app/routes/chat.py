
from datetime import date, time

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.services.embedding import generate_embedding
from app.services.vector_store import search_similar_chunks
from app.services.llm import generate_chat_response
from app.services.chat_memory import (
    save_message,
    get_chat_history,
    save_booking_status,
    get_booking_status
)

from app.schemas.booking import BookingChatRequest

from app.services.booking import (
    extract_booking_details,
    get_missing_booking_fields,
    get_next_booking_question,
    create_booking_confirmation,
    save_interview_booking
)

from app.db.database import get_db


router = APIRouter(prefix="/chat", tags=["Chat"])


class RetrieveRequest(BaseModel):
    question: str
    document_id: int


class AskRequest(BaseModel):
    question: str
    document_id: int
    session_id: str = Field(min_length=1)


@router.post("/retrieve")
def retrieve_documents(request: RetrieveRequest):

    query_embedding = generate_embedding(request.question)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        document_id=request.document_id,
        limit=5
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant document chunks found"
        )

    return {
        "question": request.question,
        "document_id": request.document_id,
        "total_results": len(results),
        "results": [
            {
                "score": point.score,
                "text": point.payload["text"]
            }
            for point in results
        ]
    }


@router.post("/ask")
def ask_question(request: AskRequest):

    query_embedding = generate_embedding(request.question)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        document_id=request.document_id,
        limit=5
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant document chunks found"
        )

    context = "\n\n".join(
        point.payload["text"]
        for point in results
    )

    history = get_chat_history(request.session_id)

    messages = [
        {
            "role": "system",
            "content": f"""
            You are a helpful document assistant.

            Answer the user's question using ONLY the
            information provided in the document context.

            You can use conversation history to understand
            follow-up questions.

            Do not use conversation history as a source
            of factual information if it is not supported
            by the document context.

            If the answer is not available in the context,
            clearly say that the document does not contain
            enough information.

            Document Context:
            {context}
            """
        }
    ]

    for message in history:

        role, content = message.split("|", 1)

        if role in {"user", "assistant"}:
            messages.append({
                "role": role,
                "content": content
            })

    messages.append({
        "role": "user",
        "content": request.question
    })

    answer = generate_chat_response(messages)

    save_message(
        request.session_id,
        "user",
        request.question
    )

    save_message(
        request.session_id,
        "assistant",
        answer
    )

    return {
        "question": request.question,
        "document_id": request.document_id,
        "session_id": request.session_id,
        "answer": answer,
        "retrieved_chunks": len(results)
    }


@router.post("/book-interview")

@router.post("/book-interview")
def book_interview(
    request: BookingChatRequest,
    db: Session = Depends(get_db)
):

    booking_session_id = f"booking_{request.session_id}"

    # STEP 1: Check whether booking is already completed
    existing_booking_id = get_booking_status(booking_session_id)

    if existing_booking_id:
        return {
            "session_id": request.session_id,
            "answer": (
                "Your interview has already been booked successfully.\n\n"
                f"Booking ID: {existing_booking_id}\n"
                "No duplicate booking was created."
            )
        }

    history = get_chat_history(booking_session_id)

    messages = []

    for message in history:

        role, content = message.split("|", 1)

        if role in {"user", "assistant"}:
            messages.append({
                "role": role,
                "content": content
            })

    messages.append({
        "role": "user",
        "content": request.message
    })

    # STEP 2: Extract booking information
    details = extract_booking_details(messages)

    print("BOOKING DETAILS:", details)

    # STEP 3: Find missing booking information
    missing_fields = get_missing_booking_fields(details)

    if missing_fields:

        answer = get_next_booking_question(missing_fields)

    else:

        # STEP 4: Check whether confirmation was already shown
        confirmation_was_shown = any(
            role == "assistant"
            and content.startswith(
                "Please review your interview booking details:"
            )
            for role, content in (
                message.split("|", 1)
                for message in history
            )
        )

        if details.get("user_confirmed") and confirmation_was_shown:

            try:

                details["interview_date"] = date.fromisoformat(
                    details["interview_date"]
                )

                details["interview_time"] = time.fromisoformat(
                    details["interview_time"]
                )

                booking = save_interview_booking(
                    db,
                    details
                )

                # STEP 5: Save completed booking status in Redis
                save_booking_status(
                    booking_session_id,
                    booking.id
                )

                answer = (
                    "Your interview has been successfully booked!\n\n"
                    f"Booking ID: {booking.id}\n"
                    f"Name: {booking.candidate_name}\n"
                    f"Email: {booking.email}\n"
                    f"Date: {booking.interview_date}\n"
                    f"Time: {booking.interview_time}\n\n"
                    "Thank you!"
                )

            except (ValueError, TypeError):

                db.rollback()

                answer = (
                    "I couldn't process the date or time. "
                    "Please provide a valid date and time."
                )

            except Exception:

                db.rollback()

                raise HTTPException(
                    status_code=500,
                    detail="Unable to save the interview booking"
                )

        else:

            answer = create_booking_confirmation(details)

    # STEP 6: Save conversation in Redis
    save_message(
        booking_session_id,
        "user",
        request.message
    )

    save_message(
        booking_session_id,
        "assistant",
        answer
    )

    return {
        "session_id": request.session_id,
        "answer": answer
    }
