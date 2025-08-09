import React, { useState } from 'react';
import './index.css';

const PostRidePage = ({ onNavigateHome, onRidePosted }) => {
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [seats, setSeats] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newRide = { from, to, date, time, seats };
    
    // In a real app, you would send this to a backend API
    console.log('New ride posted:', newRide);
    
    // Notify the parent component and navigate home
    onRidePosted(newRide); 
  };

  return (
    <div className="post-ride-page-container">
      <div className="post-ride-form-card">
        <h2 className="post-ride-page-title">Offer a Ride</h2>
        <form onSubmit={handleSubmit} className="post-ride-form">
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="from">Starting Location</label>
              <input
                id="from"
                type="text"
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                className="form-input"
                placeholder="e.g., New York, NY"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="to">Destination</label>
              <input
                id="to"
                type="text"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="form-input"
                placeholder="e.g., Boston, MA"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="date">Date</label>
              <input
                id="date"
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="time">Departure Time</label>
              <input
                id="time"
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="seats">Available Seats</label>
              <input
                id="seats"
                type="number"
                value={seats}
                onChange={(e) => setSeats(e.target.value)}
                className="form-input"
                min="1"
                max="8"
                required
              />
            </div>
          </div>
          <button type="submit" className="submit-button">
            Post Your Ride
          </button>
        </form>
         <a href="#" onClick={(e) => { e.preventDefault(); onNavigateHome(); }} className="back-link">
          &larr; Back to Home
        </a>
      </div>
    </div>
  );
};

export default PostRidePage;
