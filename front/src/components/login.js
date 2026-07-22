import React, { useState } from 'react';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [{ username, email, password }, setForm] = useState({ username: '', email: '', password: '' });
    const [msg, setMsg] = useState('');

    const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(`http://localhost:8000/${isLogin ? 'auth/token' : 'users/register'}`, {
                method: 'POST',
                headers: { 'Content-Type': isLogin ? 'application/x-www-form-urlencoded' : 'application/json' },
                body: isLogin 
                    ? new URLSearchParams({ username, password }) 
                    : JSON.stringify({ email, username, password, full_name: username })
            });
            const data = await res.json();

            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('username', username);
                window.location.href = "/"; 
            } else if (!isLogin && res.ok) {
                setMsg("Реєстрація успішна!"); setIsLogin(true);
            } else setMsg(data.detail || "Помилка");
        } catch { setMsg("Помилка з'єднання"); }
    };

    return (
        <div className="auth-container"><div className="auth-card">
            <h1 className="logo">ServMine</h1>
            <h2>{isLogin ? "Вхід" : "Реєстрація"}</h2>
            <div style={{ color: isLogin ? 'red' : 'green', textAlign: 'center' }}>{msg}</div>
            
            <form onSubmit={handleSubmit}>
                {!isLogin && <input type="email" name="email" placeholder="Email" onChange={handleChange} required />}
                <input type="text" name="username" placeholder="Логін" onChange={handleChange} required />
                <input type="password" name="password" placeholder="Пароль" onChange={handleChange} required />
                <button type="submit" className="auth-btn">{isLogin ? "Увійти" : "Створити аккаунт"}</button>
            </form>

            <p onClick={() => { setIsLogin(!isLogin); setMsg(''); }} className="toggle-auth" style={{cursor: 'pointer'}}>
                {isLogin ? "Немає аккаунту? Реєстрація" : "Вже є аккаунт? Увійти"}
            </p>
        </div></div>
    );
};

export default Login;
