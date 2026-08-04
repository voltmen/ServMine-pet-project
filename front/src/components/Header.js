import React, { useState, useEffect } from "react";
import Login from "./login";

export default function Header({ setCurrentPage }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const toggleModal = () => setIsModalOpen(!isModalOpen);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setIsLoggedIn(false);
    if (setCurrentPage) setCurrentPage('home');
    window.location.reload();
  };

  return (
    <header style={{ background: '#ffffff', padding: '15px 0', borderBottom: '1px solid #eaeaea' }}>
      <div className="wrapper" style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        
        <ul className="nav" style={{ display: 'flex', listStyle: 'none', gap: '35px', margin: 0, padding: 0, alignItems: 'center' }}>
          
          <li 
            onClick={() => setCurrentPage && setCurrentPage('home')} 
            style={{ color: '#000', cursor: 'pointer', textTransform: 'uppercase', fontWeight: '550', fontSize: '15px' }}
          >
            home
          </li>
          
          <li 
            onClick={() => setCurrentPage && setCurrentPage('about')}
            style={{ color: '#000', cursor: 'pointer', textTransform: 'uppercase', fontWeight: '550', fontSize: '15px' }}
          >
            about us
          </li>
          
          {!isLoggedIn && (
            <li 
              onClick={toggleModal} 
              style={{ 
                color: '#28a745', 
                cursor: 'pointer', 
                textTransform: 'uppercase', 
                fontWeight: '550',
                padding: '10px 15px',
                borderRadius: '20px',
                fontSize: '15px'
              }}
            >
              login
            </li>
          )}
          
          {isLoggedIn && (
            <>
              <li 
                onClick={() => setCurrentPage && setCurrentPage('profile')} 
                style={{ color: '#000', cursor: 'pointer', textTransform: 'uppercase', fontWeight: '550', fontSize: '15px' }}
              >
                my profile
              </li>
              <li 
                onClick={handleLogout} 
                style={{ 
                  color: '#dc3545', 
                  cursor: 'pointer', 
                  textTransform: 'uppercase', 
                  fontWeight: '550',
                  marginLeft: '20px',
                  fontSize: '15px'
                }}
              >
                logout
              </li>
            </>
          )}
        </ul>
      </div>

      <div className='presentation'></div>

      {isModalOpen && (
        <div className="modal-overlay" onClick={toggleModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={toggleModal}>×</button>
            <Login /> 
          </div>
        </div>
      )}
    </header>
  );
}