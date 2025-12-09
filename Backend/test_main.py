from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from main import app

client = TestClient(app)

# --- MOCK DATA ---
mock_google_response = {
    "form_id": "test_form_id_123",
    "form_url": "https://docs.google.com/forms/d/e/123/viewform"
}

# --- TESTS ---

def test_read_root():
    """Test the root endpoint to ensure API is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Quiz System Backend is Running"}

@patch("main.create_google_form")  # Mocking the sync Google function
@patch("main.quizzes_collection.insert_one", new_callable=AsyncMock) # Mocking Async DB Insert
@patch("main.quizzes_collection.find_one", new_callable=AsyncMock)   # Mocking Async DB Find
def test_create_quiz(mock_find, mock_insert, mock_google):
    """
    Test creating a quiz.
    Mocks Google API to avoid real network calls.
    Mocks MongoDB to avoid real database writes.
    """
    # 1. Setup Google Mock
    mock_google.return_value = mock_google_response
    
    # 2. Setup DB Insert Mock
    mock_insert.return_value.inserted_id = "mock_obj_id"
    
    # 3. Setup DB Find Mock (Critical: Must include all fields required by QuizDB model)
    mock_find.return_value = {
        "_id": "mock_obj_id",
        "title": "Unit Test Quiz",
        "status": "draft",
        "form_id": mock_google_response["form_id"], # Fixed: Added missing field
        "form_url": mock_google_response["form_url"],
        "questions": []
    }

    # 4. Make Request
    payload = {
        "title": "Unit Test Quiz",
        "questions": [
            {
                "text": "Is this a test?",
                "options": ["Yes", "No"],
                "correct_answer": "Yes"
            }
        ]
    }
    response = client.post("/quizzes/", json=payload)

    # 5. Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Unit Test Quiz"
    assert data["form_url"] == mock_google_response["form_url"]
    assert data["form_id"] == mock_google_response["form_id"]
    
    # Verify Google API was called exactly once
    mock_google.assert_called_once()

@patch("main.get_quiz_by_id", new_callable=AsyncMock)
def test_invalid_transition(mock_get_quiz):
    """
    Test the 'Trick Logic': Cannot approve a quiz that is already approved.
    """
    # Simulate fetching a quiz that is ALREADY approved
    mock_get_quiz.return_value = {
        "_id": "existing_id",
        "title": "Already Approved Quiz",
        "status": "approved", 
        "form_id": "123",
        "form_url": "http://google.com",
        "questions": []
    }
    
    response = client.post(
        "/quizzes/existing_id/approve", 
        json={"emails": ["test@example.com"]}
    )
    
    # Should fail with 400 Bad Request
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid Transition: Quiz is already approved."

@patch("main.get_quiz_by_id", new_callable=AsyncMock)
def test_get_quiz_not_found(mock_get):
    """Test getting a non-existent quiz."""
    mock_get.return_value = None 
    
    response = client.get("/quizzes/non_existent_id")
    assert response.status_code == 404