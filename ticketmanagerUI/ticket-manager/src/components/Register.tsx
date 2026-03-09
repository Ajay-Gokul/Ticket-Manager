import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../services/api";
import "./Auth.css";

const Register: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await authService.register({
        Name: name,
        Email: email,
        Password: password,
      });
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-visual">
        <div className="visual-content">
          <img src="/logo.png" alt="Logo" className="visual-logo" />
          <h1>Join the Network</h1>
          <p>
            Register today to gain access to our comprehensive tools. Manage
            support requests, collaborate with team members, and ensure no
            ticket goes unhandled.
          </p>
        </div>
      </div>

      <div className="auth-form-container">
        <div className="auth-form-content">
          <h2>Get Started</h2>
          <p className="subtitle">
            Create your account to start managing tickets
          </p>

          {error && <div className="error-box">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="regName">Username</label>
              <input
                type="text"
                id="regName"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="Enter your name"
              />
            </div>
            <div className="form-group">
              <label htmlFor="regEmail">Work Email</label>
              <input
                type="email"
                id="regEmail"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="name@company.com"
              />
            </div>
            <div className="form-group">
              <label htmlFor="regPassword">Password</label>
              <input
                type="password"
                id="regPassword"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Min. 8 characters"
              />
            </div>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Creating Account..." : "Complete Registration"}
            </button>
          </form>

          <div className="auth-nav">
            Already have an account?{" "}
            <Link to="/login">Sign in to existing account</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
