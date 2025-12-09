import traceback
from fastapi import FastAPI, HTTPException, status
from typing import List
from bson import ObjectId
# --- NEW IMPORT FOR CORS ---
from fastapi.middleware.cors import CORSMiddleware 
# ---------------------------
from models import QuizCreateRequest, QuizDB, ApproveRequest
# Add 'send_email_via_gmail' to the import list
from google_svc import create_google_form, delete_google_form, get_drive_service, send_email_via_gmail
from database import quizzes_collection, get_quiz_by_id
from google_svc import create_google_form, delete_google_form, get_drive_service

app = FastAPI(title="Google Forms Quiz System")

# --- ADD THIS BLOCK TO FIX 405 ERROR ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows ALL origins (React, Postman, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allows ALL methods (GET, POST, OPTIONS, DELETE)
    allow_headers=["*"],  # Allows ALL headers
)
# ---------------------------------------

@app.get("/__health-check__")
def health_check():
    """Endpoint to verify API and service account functionality."""
    try:
        drive_service = get_drive_service()
        drive_service.about().get(fields="user").execute()
        return {"status": "ok", "message": "Google Drive API connection is successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google API health check failed: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Quiz System Backend is Running"}

# --- 2.5 GET SINGLE QUIZ (Added to complete requirements) ---
@app.get("/quizzes/{quiz_id}", response_model=QuizDB)
async def get_quiz(quiz_id: str):
    """Get details for a specific quiz."""
    quiz = await get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@app.post("/quizzes/", response_model=QuizDB, status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz_in: QuizCreateRequest):
    """Takes questions, creates a Google Form, saves to MongoDB as DRAFT."""
    try:
        print(f"--- [DEBUG] Creating Quiz: {quiz_in.title} ---")
        google_res = create_google_form(quiz_in.title, quiz_in.questions, quiz_in.shuffle_questions, quiz_in.shuffle_options)

        
        
        new_quiz = QuizDB(
            title=quiz_in.title,
            status="draft",
            form_id=google_res["form_id"],
            form_url=google_res["form_url"],
            questions=quiz_in.questions
        )
        
        new_quiz_dict = new_quiz.model_dump(by_alias=True, exclude=["id"])
        result = await quizzes_collection.insert_one(new_quiz_dict)
        
        created_quiz = await quizzes_collection.find_one({"_id": result.inserted_id})
        return created_quiz

    except Exception as e:
        print("\n!!! ERROR !!!")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create quiz. Reason: {str(e)}")

@app.get("/quizzes/", response_model=List[QuizDB])
async def list_quizzes():
    quizzes = await quizzes_collection.find().to_list(100)
    return quizzes

@app.post("/quizzes/{quiz_id}/approve")
async def approve_quiz(quiz_id: str, payload: ApproveRequest):
    """Transition: Draft -> Approved. Triggers email and updates DB."""
    quiz = await get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if quiz.get("status") == "approved":
        raise HTTPException(status_code=400, detail="Invalid Transition: Quiz is already approved.")
    
    # 1. Update DB Status
    await quizzes_collection.update_one({"_id": quiz["_id"]}, {"$set": {"status": "approved"}})
    
    # 2. Send Real Emails
    print(f"--- Sending emails to {len(payload.emails)} recipients... ---")
    
    email_subject = f"Quiz Invitation: {quiz['title']}"
    email_body = f"""
    Hello,
    
    You have been invited to take the following quiz: "{quiz['title']}".
    
    Please click the link below to start:
    {quiz['form_url']}
    
    Good luck!
    """
    
    # Call the Google Service function
    send_email_via_gmail(payload.emails, email_subject, email_body)

    return {"message": "Quiz approved and emails sent.", "status": "approved"}

@app.delete("/quizzes/{quiz_id}", status_code=204)
async def delete_quiz(quiz_id: str):
    quiz = await get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    if "form_id" in quiz and quiz["form_id"]:
        try:
            delete_google_form(quiz["form_id"])
        except Exception as e:
            print(f"Could not delete form from Google Drive: {e}")
    
    await quizzes_collection.delete_one({"_id": quiz["_id"]})
    return