import React, { useState, useEffect } from 'react';
import './index.css';

const OtpPage = ({ onNavigateHome, onVerificationSuccess }) => {
  const [otp, setOtp] = useState('');

  // In a real app, an OTP would be sent to the user's mobile/email.
  // For this demo, we'll log a fake OTP to the console.
  useEffect(() => {
    const fakeOtp = Math.floor(100000 + Math.random() * 900000);
    console.log(`Your verification OTP is: ${fakeOtp}`);
    alert(`Your verification OTP is: ${fakeOtp}`); // Show alert for easy testing
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, you would verify the OTP against your backend.
    // For this demo, any 6-digit number will work.
    if (otp.length === 6) {
      console.log('OTP Verified:', otp);
      onVerificationSuccess();
    } else {
      alert('Please enter a valid 6-digit OTP.');
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-form-card">
        <h2 className="auth-page-title">Verify Your Account</h2>
        <p className="otp-page-subtitle">
          An OTP has been sent to your registered mobile number.
        </p>
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            placeholder="______"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
            className="auth-input otp-input"
            maxLength="6"
            required
          />
          <button type="submit" className="auth-button">
            Verify
          </button>
        </form>
        <div className="auth-link-container">
          <a href="#" onClick={(e) => { e.preventDefault(); onNavigateHome(); }} className="auth-link">
            &larr; Back to Home
          </a>
        </div>
      </div>
    </div>
  );
};

export default OtpPage;
