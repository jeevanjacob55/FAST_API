import React, { useState } from 'react';
import './index.css';

const SignUpPage = ({ onNavigateHome, onNavigateToLogin, onSignUpSubmit }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [mobileNumber, setMobileNumber] = useState('');
  const [aadharNumber, setAadharNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mobileNumber.length !== 10) {
      alert("Please enter a valid 10-digit mobile number.");
      return;
    }
    if (aadharNumber.length !== 12) {
      alert("Please enter a valid 12-digit Aadhar number.");
      return;
    }
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    console.log('Sign up attempt:', { name, email, mobileNumber, aadharNumber });
    onSignUpSubmit(); // This will now navigate to the OTP page
  };

  return (
    <div className="auth-page-container">
      <div className="auth-form-card">
        <h2 className="auth-page-title">Create Your Account</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} className="auth-input" required />
          <input type="email" placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)} className="auth-input" required />
          <input type="tel" placeholder="Mobile Number (10 digits)" value={mobileNumber} onChange={(e) => setMobileNumber(e.target.value.replace(/\D/g, ''))} className="auth-input" maxLength="10" required />
          <input type="text" placeholder="Aadhar Number (12 digits)" value={aadharNumber} onChange={(e) => setAadharNumber(e.target.value.replace(/\D/g, ''))} className="auth-input" maxLength="12" required />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="auth-input" required />
          <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="auth-input" required />
          <button type="submit" className="auth-button">
            Sign Up & Get OTP
          </button>
        </form>
        <div className="auth-link-container">
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigateToLogin(); }} className="auth-link">
            Already have an account? Login
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigateHome(); }} className="auth-link">
            &larr; Back to Home
          </a>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
