import React from 'react';
import './index.css';

const LandingPage = ({ isFadingOut }) => {
  return (
    <div className={`landing-page ${isFadingOut ? 'fade-out' : ''}`}>
      <div className="landing-logo">
        <img src="/rusher-logo.png" alt="RUSHER Logo" style={{ height: '100px' }} />
      </div>
    </div>
  );
};

export default LandingPage;
