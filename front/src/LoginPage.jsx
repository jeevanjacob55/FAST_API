import React, { useState } from 'react';
import './index.css';

const LoginPage = ({ onNavigateHome, onNavigateToSignUp, onLoginSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email && password) {
      console.log('Login attempt:', { email, password });
      onLoginSubmit(); // This will now navigate to the OTP page
    } else {
      alert('Please enter both email and password.');
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-form-card">
        <h2 className="auth-page-title">Login to RUSHER</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="auth-input"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="auth-input"
            required
          />
          <button type="submit" className="auth-button">
            Get OTP
          </button>
        </form>
        <div className="auth-link-container">
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigateToSignUp(); }} className="auth-link">
            Don't have an account? Sign Up
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigateHome(); }} className="auth-link">
            &larr; Back to Home
          </a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
