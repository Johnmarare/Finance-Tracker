import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';


function Sidebar() {
    return (
        <Navbar sticky="top" className="flex-column Sidebar">
            <Nav>
                <Nav.Link href="/dashboard">Dashboard</Nav.Link>
            </Nav>
            <Nav>
                <Nav.Link href="/expenses">Expenses</Nav.Link>
            </Nav>
            <Nav>
                <Nav.Link href="/incomes">Incomes</Nav.Link>
            </Nav>
        </Navbar>
    )
}

export default Sidebar;

