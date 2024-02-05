// components/App.js

import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Expenses from './components/Expense'; // Import your Expenses component
import Income from './components/Income'; // Import your Income component

const baseurl = "http://localhost:5000";

const App = () => {
  const [currentSection, setCurrentSection] = useState('expenses');

  return (
    <div className='App'>
      <Header />
      <Container fluid>
        <div className="d-flex">
          <Sidebar />
          <main className="p-4">
            {/* Use tabs, buttons, or other navigation elements to switch between sections */}
            {/* For simplicity, I'm using buttons for demonstration purposes */}
            <button onClick={() => setCurrentSection('expenses')}>Expenses</button>
            <button onClick={() => setCurrentSection('income')}>Income</button>

            {/* Render the appropriate component based on the current section */}
            {currentSection === 'expenses' && <Expenses />}
            {currentSection === 'income' && <Income />}
          </main>
        </div>
      </Container>
    </div>
  );
};

export default App;
