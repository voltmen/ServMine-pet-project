import React, { useState, useEffect } from 'react';
import './AboutUs.css';

const AboutUs = () => {
    const [reviews, setReviews] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [news, setNews] = useState([]);

    useEffect(() => {
        
        // 1. news
        fetch('http://localhost:8000/news/minecraft')
            .then(res => res.json())
            .then(data => setNews(data))
            .catch(err => console.error("Error in the news:", err));

        // 2. reviews
        fetch('http://localhost:8000/reviews')
            .then(res => res.json())
            .then(data => setReviews(data))
            .catch(err => console.error("error reviews :", err));
    }, []); 

    const handleAddReview = (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        fetch('http://localhost:8000/reviews', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: inputValue })
        })
        .then(res => res.json())
        .then(newReview => {
            setReviews([newReview, ...reviews]);
            setInputValue("");
        })
        .catch(err => console.error("error on save", err));
    };

    return (
        <div className="about-grid-container">
            {/* ЛІВА КОЛОНКА: НОВИНИ */}
            <aside className="news-side">
                <h2>Новини Майнкрафту</h2>
                <div className="news-list">
                    {news.map(item => (
                        <a href={item.url} target="_blank" rel="noopener noreferrer" key={item.id} className="news-link">
                            <div className="news-item"> 
                                <img src={item.image_url} alt={item.title} className="news-img" />
                                <h4>{item.title}</h4>
                                <p className="news-desc">{item.description}</p>
                            </div>
                        </a>
                    ))}
                </div>
            </aside>

            <section className="about-side">
                <h1>About Our Server ServMine</h1>
                <p>We are the best server!</p>
            </section>

            <aside className="reviews-side">
                <h2>Відгуки</h2>
                <div className="reviews-list">
                    {reviews.map((rev, index) => (
                        <div key={rev.id || index} className="review-card">
                            {rev.text}
                        </div>
                    ))}
                </div>
                <form onSubmit={handleAddReview} className="review-form">
                    <input 
                        type="text" 
                        value={inputValue} 
                        onChange={(e) => setInputValue(e.target.value)} 
                        placeholder="Напиши відгук..." 
                    />
                    <button type="submit" className="auth-btn">send</button>
                </form>
            </aside>
        </div>
    );
};

export default AboutUs;
