import { useState, useEffect } from 'react';

const Profile = ({ setCurrentPage }) => { 
  const [user, setUser] = useState(null);
  const [error, setError] = useState(false); 

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      setError(true);
      return;
    }

    fetch('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(res => {
      if (!res.ok) {
        return res.json().then(err => { throw err; });
      }
      return res.json();
    })
    .then(data => {
      console.log("Data from the server:", data);
      setUser(data);
    })
    .catch(err => {
      console.error("Loading error:", err);
      
      if (err.detail === "Could not validate credentials") {
          localStorage.removeItem('token');
      }
      setError(true);
    });
  }, []); 

  if (error) {
    return (
      <div className="profile-card">
        <h2>Access restricted</h2>
        <p>It looks like your token has "expired" or you aren't logged in.</p>
        <button className="auth-btn" onClick={() => setCurrentPage('home')}>
          Home
        </button>
      </div>
    );
  }

  if (!user) return <div className="loader">Loading profile...</div>;

  return (
    <div className="profile-card">
      <h2>Особисті дані</h2>
      <div className="info-group">
        <p><strong>Your login:</strong> {user.username || "Not specified"}</p>
        <p><strong>Your Email:</strong> {user.email || "НNot specified"}</p>
      </div>
      <div className="stats-section">
        <h3>Activity</h3>
        <p>Your achievements on ServMine will appear here over time!</p>
      </div>
    </div>
  );
};

export default Profile;