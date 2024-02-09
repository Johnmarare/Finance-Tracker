import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

function Header() {
    return (
        <Navbar bg='primary' sticky='top' className='Header'>
            <Container>
                <Navbar.Brand>Fedha</Navbar.Brand>
                <Button variant="secondary" href="/logout">Log out</Button>
            </Container>
        </Navbar>
    );
}

export default Header;