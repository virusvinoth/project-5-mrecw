import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import API from '../api';


export default function Login() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({ email: '', password: '' });
  const [token, setToken] = useState('');

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post('/auth/login', formData);
      setToken(res.data.access_token);
      localStorage.setItem('token', res.data.access_token);
      alert('Login successful!');
      navigate('/home');
    } catch (err) {
      alert(err.response?.data?.detail || 'Login failed.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
      <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
      <button type="submit">Login</button>
      {token && <p>Token: {token}</p>}
    </form>
  );
}
