from fastapi import FastAPI
from pydantic import BaseModel
from app.routes.documents import router as documents_router
from app.routes.chat import router as chat_router

app = FastAPI(
    title="DocuMind AI",
    description="AI-Powered Document Assistant and Interview Scheduling API",
    version="1.0.0"
)
app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return{
        "message": "Welcome to Palm Mind AI Backend"
    }

@app.get("/about")
def  about():
    return{
        "project": "Palm Mind AI",
        "purpose":  "Document Assistant and Interview Booking",
        "status":  "In development"
    }

#pydantic schema
class Student(BaseModel):
    name:str
    age:int
    email: str
    city:str

@app.post("/students")
def create_student(student:Student):
    return{
        "message": "Student recieved successfully",
        "student_data": student
    }