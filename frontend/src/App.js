// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Expense from './pages/Expense';
import Income from './pages/Income';
import Budget from './pages/Budget';
import Signup from './pages/Signup';
import LoginPage from './pages/LoginPage';
import UserPage from './pages/UserPage'

const App = () => {
  return (
    <Router>
      <Container fluid className='App'>
        <Header />
        <Container fluid>
          <div className="d-flex">
            <Sidebar />
            <main className="p-4">
              <Routes>
                <Route path="/" element={<Expense />} />
                <Route path="/expense" element={<Expense />} />
                <Route path="/income" element={<Income />} />
                <Route path="/budget" element={<Budget />} />
                <Route path='user/:username' element={<UserPage />} />
                <Route path='login' element={<LoginPage />} />
                <Route path='signup' element={<Signup />}/>
                <Route path="*" element={<Navigate to="/" />} />
              </Routes>
            </main>
          </div>
        </Container>
      </Container>
    </Router>
  );
};

export default App;
