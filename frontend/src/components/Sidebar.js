import React, { useState } from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  return (
    <Navbar sticky="top" className={`flex-column Sidebar ${collapsed ? 'collapsed' : ''}`}>
      <Navbar.Toggle onClick={toggleSidebar} aria-controls="sidebar-nav" />
      <Navbar.Collapse id="sidebar-nav">
        <Nav className="flex-column">
          <Nav.Link href="/dashboard">Dashboard</Nav.Link>
          <Nav.Link href="/expense">Expenses</Nav.Link>
          <Nav.Link href="/income">Incomes</Nav.Link>
          <Nav.Link href="/budget">Budget</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Sidebar;
