import axios from 'axios';

// Ensure this matches your Backend URL (default is 8000)
const API_URL = 'http://localhost:8000';

export const api = {
  // GET: List all quizzes
  fetchAllQuizzes: async () => {
    const response = await axios.get(`${API_URL}/quizzes/`);
    return response.data;
  },

  // POST: Create a new quiz
createQuiz: async (title, questions, shuffleQuestions, shuffleOptions) => {
    return axios.post(`${API_URL}/quizzes/`, { 
        title, 
        questions,
        shuffle_questions: shuffleQuestions, // Send to backend
        shuffle_options: shuffleOptions      // Send to backend
    });
  },

  // POST: Approve quiz (Trigger Email)
  approveQuiz: async (quizId, emails) => {
    const payload = { emails: emails };
    const response = await axios.post(`${API_URL}/quizzes/${quizId}/approve`, payload);
    return response.data;
  },

  // DELETE: Remove quiz
  deleteQuiz: async (quizId) => {
    await axios.delete(`${API_URL}/quizzes/${quizId}`);
  }
};