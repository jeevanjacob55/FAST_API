import React, { useState } from 'react';
import './index.css'; // Import styles

const LoginPage = ({ onNavigateHome, onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you would validate credentials here
    if (email && password) {
      console.log('Logging in with:', { email, password });
      onLoginSuccess(); // Notify App component of successful login
    } else {
      alert('Please enter both email and password.');
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-form-card">
        <h2 className="login-page-title">Login to RUSHER</h2>
        <form onSubmit={handleSubmit} className="login-page-form">
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="login-page-input"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-page-input"
            required
          />
          <button type="submit" className="login-page-button">
            Login
          </button>
        </form>
        <a href="#" onClick={(e) => { e.preventDefault(); onNavigateHome(); }} className="back-link">
          &larr; Back to Home
        </a>
      </div>
    </div>
  );
};

export default LoginPage;
