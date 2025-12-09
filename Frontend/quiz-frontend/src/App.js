import React, { useState, useEffect } from 'react';
import { api } from './api';
import './App.css'; 

function App() {
  const [quizzes, setQuizzes] = useState([]);
  const [refresh, setRefresh] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  // New Shuffle State
  const [shuffleQuestions, setShuffleQuestions] = useState(false);
  const [shuffleOptions, setShuffleOptions] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [questions, setQuestions] = useState([
    { text: '', options: '', correct_answer: '' }
  ]);

  // --- AUTO-LOAD ON STARTUP ---
  useEffect(() => {
    loadQuizzes();
  }, [refresh]);

  const loadQuizzes = async () => {
    try {
      const data = await api.fetchAllQuizzes();
      setQuizzes(data);
    } catch (err) {
      console.error("Failed to fetch quizzes");
    }
  };

  // --- VALIDATION HELPER ---
  const validateForm = () => {
    if (!title.trim()) {
      alert("⚠️ Please enter a Quiz Title.");
      return false;
    }
    if (questions.length === 0) {
      alert("⚠️ Please add at least one question.");
      return false;
    }
    for (let i = 0; i < questions.length; i++) {
      if (!questions[i].text.trim()) {
        alert(`⚠️ Question ${i + 1} cannot be empty.`);
        return false;
      }
      if (!questions[i].options.trim()) {
        alert(`⚠️ Question ${i + 1} must have options.`);
        return false;
      }
      if (!questions[i].correct_answer.trim()) {
        alert(`⚠️ Please select a correct answer for Question ${i + 1}.`);
        return false;
      }
    }
    return true;
  };

  // --- HANDLERS ---
  const handlePreview = () => {
    if (!validateForm()) return;
    setShowPreview(true);
  };

  const handleAddQuestion = () => {
    setQuestions([...questions, { text: '', options: '', correct_answer: '' }]);
  };

  const handleRemoveQuestion = (index) => {
    const newQuestions = questions.filter((_, i) => i !== index);
    setQuestions(newQuestions);
  };

  const handleQuestionChange = (index, field, value) => {
    const newQuestions = [...questions];
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setShowPreview(false);
    
    const formattedQuestions = questions.map(q => ({
      text: q.text,
      options: q.options.split(',').map(o => o.trim()).filter(o => o !== ""),
      correct_answer: q.correct_answer
    }));

    try {
      // Pass shuffle settings to the API
      await api.createQuiz(title, formattedQuestions, shuffleQuestions, shuffleOptions);
      alert("✅ Quiz Created Successfully!");
      
      // Reset Form
      setTitle('');
      setQuestions([{ text: '', options: '', correct_answer: '' }]);
      setShuffleQuestions(false);
      setShuffleOptions(false);
      setRefresh(!refresh); 
    } catch (err) {
      alert("❌ Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (id) => {
    const emailStr = prompt("Enter student emails (comma separated):", "student@example.com");
    if (!emailStr) return;
    try {
      await api.approveQuiz(id, emailStr.split(',').map(e => e.trim()));
      alert("📧 Quiz Approved & Emails Sent!");
      setRefresh(!refresh);
    } catch (err) {
      alert("❌ Error: " + (err.response?.data?.detail || "Failed"));
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this quiz?")) return;
    try {
      await api.deleteQuiz(id);
      setRefresh(!refresh);
    } catch (err) {
      alert("Delete failed");
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🎓 Google Forms Quiz System</h1>
        <p className="subtitle">Automated Quiz Generation & Approval Workflow</p>
      </header>

      {/* --- CREATE QUIZ FORM --- */}
      <section className="card">
        <h2>1. Create New Quiz</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Quiz Title</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="e.g. Final Semester Exam" />
          </div>
          
          <h3>Questions</h3>
          {questions.map((q, index) => {
            const currentOptions = q.options.split(',').map(o => o.trim()).filter(o => o !== "");

            return (
              <div key={index} className="question-box">
                <div className="q-header">
                  <span>Question {index + 1}</span>
                  {questions.length > 1 && (
                    <button type="button" onClick={() => handleRemoveQuestion(index)} className="btn-text-danger">Remove</button>
                  )}
                </div>
                
                <input 
                  placeholder="Question Text" 
                  value={q.text} 
                  onChange={e => handleQuestionChange(index, 'text', e.target.value)} 
                  style={{marginBottom: '10px'}}
                />
                
                <input 
                  placeholder="Options (comma separated: A, B, C)" 
                  value={q.options} 
                  onChange={e => handleQuestionChange(index, 'options', e.target.value)} 
                  style={{marginBottom: '10px'}}
                />

                {/* Correct Answer Dropdown */}
                <div className="form-group" style={{marginBottom: 0}}>
                    <label style={{fontSize: '0.9em', color: '#666', marginBottom: '5px', display:'block'}}>Select Correct Answer:</label>
                    <select 
                        value={q.correct_answer}
                        onChange={e => handleQuestionChange(index, 'correct_answer', e.target.value)}
                        style={{
                            width: '100%', 
                            padding: '12px', 
                            borderRadius: '6px', 
                            border: '1px solid #ced0d4',
                            backgroundColor: '#fff',
                            fontSize: '14px',
                            color: '#1c1e21',
                        }}
                    >
                        <option value="">-- Select Answer --</option>
                        {currentOptions.length > 0 ? (
                            currentOptions.map((opt, i) => (
                                <option key={i} value={opt}>{opt}</option>
                            ))
                        ) : (
                            <option disabled>Type options above first...</option>
                        )}
                    </select>
                </div>
              </div>
            );
          })}

          {/* --- SHUFFLE SETTINGS --- */}
          <div style={{display: 'flex', gap: '20px', margin: '20px 0', padding: '15px', background: '#f8f9fa', borderRadius: '8px', border: '1px solid #e9ecef'}}>
            <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', fontWeight: 500}}>
                <input 
                    type="checkbox" 
                    checked={shuffleQuestions} 
                    onChange={e => setShuffleQuestions(e.target.checked)} 
                    style={{width: 'auto', marginRight: '8px', marginBottom: 0}}
                />
                Shuffle Questions
            </label>
            <label style={{display: 'flex', alignItems: 'center', cursor: 'pointer', fontWeight: 500}}>
                <input 
                    type="checkbox" 
                    checked={shuffleOptions} 
                    onChange={e => setShuffleOptions(e.target.checked)} 
                    style={{width: 'auto', marginRight: '8px', marginBottom: 0}}
                />
                Shuffle Options
            </label>
          </div>
          
          <div className="form-actions">
            <button type="button" onClick={handleAddQuestion} className="btn-secondary">+ Add Question</button>
            <button type="button" onClick={handlePreview} className="btn-info">👁️ Preview</button>
            <button type="submit" className="btn-primary" disabled={loading}>{loading ? "Generating..." : "Create Quiz"}</button>
          </div>
        </form>
      </section>

      {/* --- DASHBOARD --- */}
      <section className="card">
        <h2>2. Quiz Dashboard</h2>
        {quizzes.length === 0 ? (
           <div className="empty-state">
             <p>No quizzes found. Create one above!</p>
             <button onClick={() => setRefresh(!refresh)} style={{marginTop:'10px', fontSize:'0.8rem'}} className="btn-secondary">
               🔄 Refresh List
             </button>
           </div>
        ) : (
          <table className="quiz-table">
            <thead>
              <tr><th>Title</th><th>Status</th><th>Google Form</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {quizzes.map(q => (
                <tr key={q._id}>
                  <td><strong>{q.title}</strong></td>
                  <td><span className={`status-badge ${q.status}`}>{q.status.toUpperCase()}</span></td>
                  <td><a href={q.form_url} target="_blank" rel="noreferrer" className="link-form">Open Form ↗</a></td>
                  <td>
                    {q.status === 'draft' && <button onClick={() => handleApprove(q._id)} className="btn-approve">Approve</button>}
                    <button onClick={() => handleDelete(q._id)} className="btn-delete">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* --- PREVIEW MODAL --- */}
      {showPreview && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header"><h2>Preview</h2><button onClick={() => setShowPreview(false)} className="btn-close">×</button></div>
            <div className="modal-body">
              {questions.map((q, index) => (
                <div key={index} className="preview-question-box">
                  <p><strong>{index + 1}. {q.text}</strong></p>
                  <div className="preview-options">
                    {q.options.split(',').map((opt, i) => {
                       const val = opt.trim();
                       const isCorrect = val === q.correct_answer;
                       return (
                         <div 
                           key={i} 
                           className="preview-option-row"
                           style={{color: isCorrect ? 'green' : 'black', fontWeight: isCorrect ? 'bold' : 'normal'}}
                         >
                           <input type="radio" disabled checked={isCorrect} /> 
                           <span>{val} {isCorrect ? " (Correct)" : ""}</span>
                         </div>
                       )
                    })}
                  </div>
                </div>
              ))}
            </div>
            <div className="modal-footer"><button onClick={handleSubmit} className="btn-primary">Create Quiz Now</button></div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;