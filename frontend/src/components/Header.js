import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';

function Header() {
    return (
        <Navbar bg='primary' sticky='top' className='Header'>
            <Container>
                <Navbar.Brand href='#home'>Fedha</Navbar.Brand>
                <button href="/login">Log in</button>
            </Container>
        </Navbar>
    );
}

export default Header;