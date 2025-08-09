import React, { useState } from 'react';
import './index.css';
import LoginPage from './LoginPage'; // Import the new LoginPage component

import { Car, MapPin, Calendar, Users, Search, ShieldCheck, Leaf, PiggyBank, Star, UserCircle } from 'lucide-react';

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

const HomePage = () => {
  const [rides, setRides] = useState([
    {
      id: 1,
      driver: 'Alice',
      avatar: 'https://placehold.co/100x100/a3e635/44403c?text=A',
      from: 'New York, NY',
      to: 'Boston, MA',
      departureTime: '08:00 AM',
      arrivalTime: '12:00 PM',
      price: 30,
      seats: 2,
      rating: 5,
    },
    {
      id: 2,
      driver: 'Elvin',
      avatar: 'https://placehold.co/100x100/f97316/ffffff?text=E',
      from: 'Los Angeles, CA',
      to: 'San Francisco, CA',
      departureTime: '09:30 AM',
      arrivalTime: '04:30 PM',
      price: 45,
      seats: 3,
      rating: 4,
    },
    {
      id: 3,
      driver: 'Charlie',
      avatar: 'https://placehold.co/100x100/fde047/44403c?text=C',
      from: 'Chicago, IL',
      to: 'Detroit, MI',
      departureTime: '07:15 AM',
      arrivalTime: '12:30 PM',
      price: 25,
      seats: 1,
      rating: 5,
    },
     {
      id: 4,
      driver: 'Diana',
      avatar: 'https://placehold.co/100x100/f9a8d4/44403c?text=D',
      from: 'Houston, TX',
      to: 'Austin, TX',
      departureTime: '10:00 AM',
      arrivalTime: '01:00 PM',
      price: 20,
      seats: 3,
      rating: 4,
    },
  ]);

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
              <input 
                type="text" 
                placeholder="From"
                value={fromLocation}
                onChange={(e) => setFromLocation(e.target.value)}
                className="input-field"
              />
            </div>
            <div className="input-group">
              <MapPin className="input-icon w-5 h-5" />
              <input 
                type="text" 
                placeholder="To"
                value={toLocation}
                onChange={(e) => setToLocation(e.target.value)}
                className="input-field"
              />
            </div>
            <div className="input-group">
              <Calendar className="input-icon w-5 h-5" />
              <input 
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="input-field"
              />
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
              <div className="info-icon-wrapper">
                <Search className="info-icon" />
              </div>
              <h3 className="info-title">1. Find a Ride</h3>
              <p className="info-text">Enter your destination and find rides that match your schedule.</p>
            </div>
            <div className="info-item">
              <div className="info-icon-wrapper">
                <Car className="info-icon" />
              </div>
              <h3 className="info-title">2. Book & Pay</h3>
              <p className="info-text">Book your seat and pay securely through our platform.</p>
            </div>
            <div className="info-item">
              <div className="info-icon-wrapper">
                <Users className="info-icon" />
              </div>
              <h3 className="info-title">3. Travel Together</h3>
              <p className="info-text">Meet your driver, enjoy the ride, and make new friends.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="why-us" className="why-us-section">
        <div className="container">
          <h2 className="section-title">Why RideShare?</h2>
          <div className="why-us-grid">
            <div className="why-us-item">
              <PiggyBank className="info-icon text-blue-600" />
              <h3 className="info-title">Save Money</h3>
              <p className="info-text">Share the cost of travel. It's cheaper than a train or flying.</p>
            </div>
            <div className="why-us-item">
              <Leaf className="info-icon text-green-500" />
              <h3 className="info-title">Eco-Friendly</h3>
              <p className="info-text">Fewer cars on the road means a smaller carbon footprint.</p>
            </div>
            <div className="why-us-item">
              <ShieldCheck className="info-icon text-red-500" />
              <h3 className="info-title">Safe & Secure</h3>
              <p className="info-text">We verify profiles and our rating system builds trust.</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default function App() {
  const [page, setPage] = useState('home'); // 'home' or 'login'
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    setPage('home'); // Navigate to home after successful login
  };

  return (
    <div>
      <header className="header">
        <div className="container">
          <nav className="nav">
            <div className="logo-container">
              <Car className="w-8 h-8 text-blue-600" />
              <span className="logo-text">RUSHER</span>
            </div>
            <div className="nav-links">
              <a href="#" onClick={(e) => { e.preventDefault(); setPage('home'); }}>Find a Ride</a>
              <a href="#how-it-works">How It Works</a>
              <a href="#why-us">Why Choose Us</a>
            </div>
            <div className="header-buttons">
                {isLoggedIn ? (
                    <button className="button-primary">
                        <UserCircle style={{display: 'inline-block', verticalAlign: 'middle', marginRight: '8px'}}/>
                        My Account
                    </button>
                ) : (
                    <>
                        <button className="button-login" onClick={() => setPage('login')}>
                            Login
                        </button>
                        <button className="button-primary">
                            Post a Ride
                        </button>
                    </>
                )}
            </div>
          </nav>
        </div>
      </header>
      
      {page === 'home' && <HomePage />}
      {page === 'login' && <LoginPage onNavigateHome={() => setPage('home')} onLoginSuccess={handleLoginSuccess} />}

      <footer className="footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} RUSHER. All rights reserved.</p>
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
