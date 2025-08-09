import React, { useState, useEffect } from 'react';
import './index.css';
import LandingPage from './LandingPage';
import LoginPage from './LoginPage';
import SignUpPage from './SignUpPage';
import OtpPage from './OtpPage'; // Import the new OtpPage component
import PostRidePage from './PostRidePage'; 

import { MapPin, Calendar, Users, Search, ShieldCheck, Leaf, PiggyBank, Star, UserCircle } from 'lucide-react';

const StarRating = ({ rating }) => {
  const stars = [];
  for (let i = 0; i < 5; i++) {
    stars.push(
      <Star
        key={i}
        className={`w-4 h-4 ${i < rating ? 'text-yellow-400' : 'text-gray-300'}`}
        fill="currentColor"
      />
    );
  }
  return <div className="star-rating">{stars}</div>;
};

const HomePage = ({ rides }) => {
  const [fromLocation, setFromLocation] = useState('');
  const [toLocation, setToLocation] = useState('');
  const [date, setDate] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    console.log(`Searching for rides from ${fromLocation} to ${toLocation} on ${date}`);
  };

  return (
    <>
      <main className="container main-content">
        <h1 className="hero-title">
          Your Journey, Shared.
        </h1>
        <p className="hero-subtitle">
          Save money, reduce your carbon footprint, and meet new people. Find a ride or offer a seat in your car.
        </p>
        
        <div id="find-ride" className="search-form-container">
          <form onSubmit={handleSearch} className="search-form">
            <div className="input-group">
              <MapPin className="input-icon w-5 h-5" />
              <input type="text" placeholder="From" value={fromLocation} onChange={(e) => setFromLocation(e.target.value)} className="input-field" />
            </div>
            <div className="input-group">
              <MapPin className="input-icon w-5 h-5" />
              <input type="text" placeholder="To" value={toLocation} onChange={(e) => setToLocation(e.target.value)} className="input-field" />
            </div>
            <div className="input-group">
              <Calendar className="input-icon w-5 h-5" />
              <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="input-field" />
            </div>
            <button type="submit" className="search-button">
              <Search className="w-5 h-5" />
              <span>Search</span>
            </button>
          </form>
        </div>
      </main>
      
      <section className="rides-section">
        <div className="container">
          <h2 className="section-title">Available Rides</h2>
          <div className="rides-grid">
            {rides.map(ride => (
              <div key={ride.id} className="ride-card">
                <div className="ride-card-content">
                  <div className="ride-card-header">
                    <img className="driver-avatar" src={ride.avatar} alt={`Driver ${ride.driver}`} />
                    <div className="driver-info">
                      <p className="driver-name">{ride.driver}</p>
                      <StarRating rating={ride.rating} />
                    </div>
                    <div className="price-info">
                      <p className="price">${ride.price}</p>
                      <p className="price-per-seat">per seat</p>
                    </div>
                  </div>
                  <div className="ride-details">
                      <div className="ride-detail-item">
                        <MapPin className="w-5 h-5 text-green-500" />
                        <div className="ride-detail-text">
                          <p className="location">{ride.from}</p>
                          <p className="time">{ride.departureTime}</p>
                        </div>
                      </div>
                      <div className="ride-detail-item">
                        <MapPin className="w-5 h-5 text-red-500" />
                        <div className="ride-detail-text">
                          <p className="location">{ride.to}</p>
                          <p className="time">{ride.arrivalTime}</p>
                        </div>
                      </div>
                      <div className="ride-detail-item">
                        <Users className="w-5 h-5 text-blue-500" />
                        <p>{ride.seats} seats available</p>
                      </div>
                  </div>
                  <button className="button-primary" style={{width: '100%', marginTop: '1.5rem', borderRadius: '0.5rem'}}>
                    Book Now
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="how-it-works" className="info-section">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="info-grid">
            <div className="info-item">
              <div className="info-icon-wrapper"><Search className="info-icon" /></div>
              <h3 className="info-title">1. Find a Ride</h3>
              <p className="info-text">Enter your destination and find rides that match your schedule.</p>
            </div>
            <div className="info-item">
              <div className="info-icon-wrapper"><img src="/rusher-logo.png" alt="Car Icon" className="info-icon" /></div>
              <h3 className="info-title">2. Book & Pay</h3>
              <p className="info-text">Book your seat and pay securely through our platform.</p>
            </div>
            <div className="info-item">
              <div className="info-icon-wrapper"><Users className="info-icon" /></div>
              <h3 className="info-title">3. Travel Together</h3>
              <p className="info-text">Meet your driver, enjoy the ride, and make new friends.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="why-us" className="why-us-section">
        <div className="container">
          <h2 className="section-title">Why RUSHR?</h2>
          <div className="why-us-grid">
            <div className="why-us-item"><PiggyBank className="info-icon text-blue-600" /><h3 className="info-title">Save Money</h3><p className="info-text">Share the cost of travel. It's cheaper than a train or flying.</p></div>
            <div className="why-us-item"><Leaf className="info-icon text-green-500" /><h3 className="info-title">Eco-Friendly</h3><p className="info-text">Fewer cars on the road means a smaller carbon footprint.</p></div>
            <div className="why-us-item"><ShieldCheck className="info-icon text-red-500" /><h3 className="info-title">Safe & Secure</h3><p className="info-text">We verify profiles and our rating system builds trust.</p></div>
          </div>
        </div>
      </section>
    </>
  );
};

export default function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isFadingOut, setIsFadingOut] = useState(false);
  
  const [page, setPage] = useState('home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [rides, setRides] = useState([
    { id: 1, driver: 'Alice', avatar: 'https://placehold.co/100x100/a3e635/44403c?text=A', from: 'New York, NY', to: 'Boston, MA', departureTime: '08:00 AM', arrivalTime: '12:00 PM', price: 30, seats: 2, rating: 5 },
    { id: 2, driver: 'Elvin', avatar: 'https://placehold.co/100x100/f97316/ffffff?text=E', from: 'Los Angeles, CA', to: 'San Francisco, CA', departureTime: '09:30 AM', arrivalTime: '04:30 PM', price: 45, seats: 3, rating: 4 },
  ]);

  useEffect(() => {
    const fadeTimer = setTimeout(() => setIsFadingOut(true), 2500);
    const loadTimer = setTimeout(() => setIsLoading(false), 3000);
    return () => { clearTimeout(fadeTimer); clearTimeout(loadTimer); };
  }, []);

  const handleVerificationSuccess = () => {
    setIsLoggedIn(true);
    setPage('home');
  };

  const handleRidePosted = (newRide) => {
    const rideWithId = { ...newRide, id: rides.length + 1, driver: 'You', avatar: 'https://placehold.co/100x100/1e40af/ffffff?text=U', rating: 5, price: 25 };
    setRides([rideWithId, ...rides]);
    setPage('home');
  };

  if (isLoading) {
    return <LandingPage isFadingOut={isFadingOut} />;
  }

  const renderPage = () => {
    switch (page) {
      case 'login':
        return <LoginPage onNavigateHome={() => setPage('home')} onNavigateToSignUp={() => setPage('signup')} onLoginSubmit={() => setPage('otp')} />;
      case 'signup':
        return <SignUpPage onNavigateHome={() => setPage('home')} onNavigateToLogin={() => setPage('login')} onSignUpSubmit={() => setPage('otp')} />;
      case 'otp':
        return <OtpPage onNavigateHome={() => setPage('home')} onVerificationSuccess={handleVerificationSuccess} />;
      case 'postRide':
        return <PostRidePage onNavigateHome={() => setPage('home')} onRidePosted={handleRidePosted} />;
      case 'home':
      default:
        return <HomePage rides={rides} />;
    }
  };

  return (
    <div className={`app-container ${!isLoading ? 'visible' : ''}`}>
      <header className="header">
        <div className="container">
          <nav className="nav">
            <div className="logo-container" onClick={() => setPage('home')} style={{cursor: 'pointer'}}>
              <img src="/rusher-logo.png" alt="RUSHER Logo" className="logo-image" />
              <span className="logo-text">RUSHR</span>
            </div>
            <div className="nav-links">
              <a href="#find-ride" onClick={(e) => { e.preventDefault(); setPage('home'); }}>Find a Ride</a>
              <a href="#how-it-works">How It Works</a>
              <a href="#why-us">Why Choose Us</a>
            </div>
            <div className="header-buttons">
                {isLoggedIn ? (
                    <>
                        <button className="button-primary" onClick={() => setPage('postRide')}>
                            Post a Ride
                        </button>
                        <button className="button-primary">
                            <UserCircle style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '8px'}}/>
                            My Account
                        </button>
                    </>
                ) : (
                    <>
                        <button className="button-login" onClick={() => setPage('login')}>
                            Login
                        </button>
                        <button className="button-signup" onClick={() => setPage('signup')}>
                            Sign Up
                        </button>
                    </>
                )}
            </div>
          </nav>
        </div>
      </header>
      
      {renderPage()}

      <footer className="footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} RUSHR. All rights reserved.</p>
          <div className="footer-links">
            <a href="#">Facebook</a>
            <a href="#">Twitter</a>
            <a href="#">Instagram</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
