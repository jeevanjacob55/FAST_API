import React, { useState, useEffect } from 'react';
import './index.css';
import LandingPage from './LandingPage';
import LoginPage from './LoginPage';
import SignUpPage from './SignUpPage';
import OtpPage from './OtpPage';
import PostRidePage from './PostRidePage'; 

import { MapPin, Calendar, Users, Search, ShieldCheck, Leaf, PiggyBank, Star, UserCircle } from 'lucide-react';

// ✅ CHANGE 1: Add a helper function to get coordinates from an address.
// This function calls the Google Maps Geocoding API.
const getCoordinates = async (address) => {
  // IMPORTANT: Store your API key in a .env file at the project root.
  // The file should contain: VITE_GOOGLE_MAPS_API_KEY="your_key_here"
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY; 
  if (!apiKey) {
    throw new Error("Google Maps API key is missing.");
  }
  const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${apiKey}`;

  const response = await fetch(url);
  const data = await response.json();

  if (data.status !== 'OK' || !data.results[0]) {
    throw new Error(`Could not find coordinates for "${address}"`);
  }

  const { lat, lng } = data.results[0].geometry.location;
  return { lat, lon: lng }; // Return in the format your backend expects
};


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


// ✅ CHANGE 2: Pass down state setters for rides, loading, and errors.
const HomePage = ({ rides, setRides, setIsLoadingRides, setErrorRides }) => {
  const [fromLocation, setFromLocation] = useState('');
  const [toLocation, setToLocation] = useState('');
  const [date, setDate] = useState('');

  // ✅ CHANGE 3: Update the search handler to be async and perform the full workflow.
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!fromLocation || !toLocation) {
      setErrorRides('Please enter both "From" and "To" locations.');
      return;
    }

    setIsLoadingRides(true);
    setErrorRides('');
    setRides([]); // Clear previous results

    try {
      // Step 1: Geocode the "From" and "To" locations.
      const startCoords = await getCoordinates(fromLocation);
      const endCoords = await getCoordinates(toLocation);

      // Step 2: Call your backend with the coordinates.
      const response = await fetch('http://127.0.0.1:8000/rides/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          leaving_from: fromLocation, // CORRECT
          going_to: toLocation,       // CORRECT
        }),
      });

      const searchResult = await response.json();

      if (!response.ok) {
        throw new Error(searchResult.detail || 'Failed to search for rides.');
      }
      
      // Update the rides list with the search results.
      setRides(searchResult);

    } catch (err) {
      setErrorRides(err.message);
      setRides([]); // Clear rides on error
    } finally {
      setIsLoadingRides(false);
    }
  };

  return (
    <>
      <main className="container main-content">
        <h1 className="hero-title">Your Journey, Shared.</h1>
        <p className="hero-subtitle">
          Save money, reduce your carbon footprint, and meet new people. Find a ride or offer a seat in your car.
        </p>
        
        <div id="find-ride" className="search-form-container">
          <form onSubmit={handleSearch} className="search-form">
            <div className="input-group">
              <MapPin className="input-icon w-5 h-5" />
              <input type="text" placeholder="From" value={fromLocation} onChange={(e) => setFromLocation(e.target.value)} className="input-field" required />
            </div>
            <div className="input-group">
              <MapPin className="input-icon w-5 h-5" />
              <input type="text" placeholder="To" value={toLocation} onChange={(e) => setToLocation(e.target.value)} className="input-field" required />
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
            {/* ✅ CHANGE 4: Update the ride card to use data from your backend. */}
            {rides.length > 0 ? rides.map(ride => (
              <div key={ride.id} className="ride-card">
                <div className="ride-card-content">
                  <div className="ride-card-header">
                    <img className="driver-avatar" src={`https://placehold.co/100x100/a3e635/44403c?text=D${ride.driver_id}`} alt={`Driver`} />
                    <div className="driver-info">
                      <p className="driver-name">Driver ID: {ride.driver_id}</p>
                      <StarRating rating={4} /> {/* Placeholder rating */}
                    </div>
                    <div className="price-info">
                      <p className="price">₹10/km</p> {/* Placeholder price */}
                      <p className="price-per-seat">approx.</p>
                    </div>
                  </div>
                  <div className="ride-details">
                    <div className="ride-detail-item">
                      <MapPin className="w-5 h-5 text-green-500" />
                      <div className="ride-detail-text">
                        <p className="location">{ride.leaving_from}</p>
                      </div>
                    </div>
                    <div className="ride-detail-item">
                      <MapPin className="w-5 h-5 text-red-500" />
                      <div className="ride-detail-text">
                        <p className="location">{ride.going_to}</p>
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
            )) : <p>No rides found. Try searching for a trip!</p>}
          </div>
        </div>
      </section>

      {/* The rest of the sections remain the same */}
      <section id="how-it-works" className="info-section">
        {/* ... */}
      </section>
      <section id="why-us" className="why-us-section">
        {/* ... */}
      </section>
    </>
  );
};


export default function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isFadingOut, setIsFadingOut] = useState(false);
  
  const [page, setPage] = useState('home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // ✅ CHANGE 5: Centralize state for rides, loading, and errors here.
  const [rides, setRides] = useState([]);
  const [isLoadingRides, setIsLoadingRides] = useState(false);
  const [errorRides, setErrorRides] = useState('');

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
    setRides([newRide, ...rides]);
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
        // ✅ CHANGE 6: Pass the state and setters down to the HomePage.
        return <HomePage 
                  rides={rides} 
                  setRides={setRides} 
                  setIsLoadingRides={setIsLoadingRides}
                  setErrorRides={setErrorRides} 
               />;
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
      
      {/* ✅ CHANGE 7: Display loading or error messages for the ride search. */}
      {isLoadingRides && <div className="container" style={{textAlign: 'center', padding: '2rem'}}><p>Searching for rides...</p></div>}
      {errorRides && <div className="container" style={{textAlign: 'center', padding: '2rem'}}><p style={{color: 'red'}}>{errorRides}</p></div>}
      
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