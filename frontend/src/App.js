import Container from 'react-bootstrap/Container';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ApiProvider from './contexts/ApiProvider';
import Header from './components/Header';
import ExpensePage from './pages/ExpensePage';
import IncomePage from './pages/IncomePage';
import BudgetPage from './pages/BudgetPage';
import UserPage from './pages/UserPage';
import LoginPage from './pages/LoginPage';

export default function App() {
  return (
    <Container fluid className="App">
      <BrowserRouter>
        <ApiProvider>
          <Header />
          <Routes>
            <Route path="/" element={<ExpensePage />} />
            <Route path="/expense" element={<ExpensePage />} />
            <Route path="/income" element={<IncomePage />} />
            <Route path="/budget" element={<BudgetPage />} />
            <Route path="/user/:username" element={<UserPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </ApiProvider>
      </BrowserRouter>
    </Container>
  );
}