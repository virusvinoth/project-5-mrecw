import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';
import './chatbot.css';

export default function Home() {
  const navigate = useNavigate();
  const [userInfo, setUserInfo] = useState(null);
  const [showChatbot, setShowChatbot] = useState(false);
  const [courses, setCourses] = useState([]);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [error, setError] = useState(null);

  const [selectedCourse, setSelectedCourse] = useState('');
  const [suggestion, setSuggestion] = useState('');
  const [suggestionLoading, setSuggestionLoading] = useState(false);
  const [suggestionError, setSuggestionError] = useState('');

  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/login');
    } else {
      API.get('/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => setUserInfo(res.data))
        .catch(() => {
          localStorage.removeItem('token');
          navigate('/login');
        });
    }
  }, [navigate, token]);

  const fetchCourses = async () => {
    setLoadingCourses(true);
    setError(null);
    try {
      const response = await API.get('/courses');
      setCourses(response.data);
    } catch (err) {
      setError('Failed to load courses.');
    } finally {
      setLoadingCourses(false);
    }
  };

  const handleChatbotToggle = () => {
    setShowChatbot(prev => !prev);
    if (!showChatbot) {
      fetchCourses(); // Load courses only when chatbot opens
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleAskSuggestion = async () => {
    if (!selectedCourse.trim()) return;
    setSuggestion('');
    setSuggestionError('');
    setSuggestionLoading(true);

    try {
      const response = await API.post('ML/mlmod', {
        topic: selectedCourse
      });
      setSuggestion(response.data.suggestion);
    } catch (err) {
      setSuggestionError('Failed to get suggestion from AI.');
    } finally {
      setSuggestionLoading(false);
    }
  };

  return (
    <div className="home-container">
      <h2>Home Page</h2>

      {userInfo ? (
        <>
          <p>Welcome, {userInfo.name}!</p>
          <p>Email: {userInfo.email}</p>
          <p>Role: {userInfo.role}</p>
        </>
      ) : (
        <p>Loading user info...</p>
      )}

      <button onClick={handleLogout}>Logout</button>

      {/* Floating Chatbot Button */}
      <div className="chatbot-button" onClick={handleChatbotToggle}>
        💬
      </div>

      {/* Chatbot Popup */}
      {showChatbot && (
        <div className="chatbot-popup">
          <div className="chatbot-header">
            <span>Course Chatbot Assistant</span>
            <button onClick={() => setShowChatbot(false)}>✖</button>
          </div>
          <div className="chatbot-body">
            <p><strong>Select a course to get AI suggestions:</strong></p>

            {loadingCourses ? (
              <p>Loading courses...</p>
            ) : error ? (
              <p style={{ color: 'red' }}>{error}</p>
            ) : (
              <>
                <select
                  value={selectedCourse}
                  onChange={(e) => setSelectedCourse(e.target.value)}
                  className="chatbot-select"
                >
                  <option value="">-- Choose a course --</option>
                  {courses.map((course, idx) => (
                    <option key={idx} value={course.title}>
                      {course.title}
                    </option>
                  ))}
                </select>

                <button
                  onClick={handleAskSuggestion}
                  className="chatbot-submit"
                  disabled={!selectedCourse}
                >
                  Get AI Suggestion
                </button>

                {suggestionLoading && <p>Thinking...</p>}
                {suggestionError && <p style={{ color: 'red' }}>{suggestionError}</p>}
                {suggestion && (
                  <div className="chatbot-suggestion">
                    <strong>Suggestion for "{selectedCourse}":</strong>
                    <p>{suggestion}</p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
