from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import List, Optional
from datetime import datetime
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Question(BaseModel):
    text: str
    options: List[str]
    correct_answer: Optional[str] = None

class QuizCreateRequest(BaseModel):
    title: str
    questions: List[Question]
    # Add these two new fields
    shuffle_questions: bool = False
    shuffle_options: bool = False

class QuizDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    status: str = "draft"
    form_url: str
    form_id: str
    questions: List[Question]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Math Quiz",
                "status": "draft",
                "form_url": "https://docs.google.com/forms/...",
                "form_id": "12345",
                "questions": []
            }
        }

class ApproveRequest(BaseModel):
    emails: List[EmailStr]