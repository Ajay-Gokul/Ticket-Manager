import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';
import './Auth.css';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const data = await authService.login({ Email: email, Password: password });
            localStorage.setItem('token', data.access_token);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-visual">
                <div className="visual-content">
                    <img src="/logo.png" alt="Logo" className="visual-logo" />
                    <h1>Ticket Manager Pro</h1>
                    <p>Streamline your support workflow, resolve issues faster, and keep your customers happy with our enterprise-grade ticketing platform.</p>
                </div>
            </div>
            
            <div className="auth-form-container">
                <div className="auth-form-content">
                    <h2>Welcome back</h2>
                    <p className="subtitle">Login to your account to continue</p>
                    
                    {error && <div className="error-box">{error}</div>}
                    
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                placeholder="name@company.com"
                                autoComplete="email"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input
                                type="password"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Enter your password"
                                autoComplete="current-password"
                            />
                        </div>
                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? 'Processing...' : 'Login to Dashboard'}
                        </button>
                    </form>
                    
                    <div className="auth-nav">
                        New to the platform? <Link to="/register">Create an account</Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
