import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Body from '../components/Body';
import InputField from '../components/InputField';
import axios from 'axios';

const baseurl = "http://localhost:5000";

export default function LoginPage() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.username) {
      errors.username = 'Username or email is required';
    }
    if (!formData.password) {
      errors.password = 'Password is required';
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const onSubmit = async (ev) => {
    ev.preventDefault();
    
    if (validateForm()) {
      try {
        const response = await axios.post(`${baseurl}/login`, {
          username: formData.username,
          password: formData.password,
        });
        console.log(response.data.message);
        // You can redirect or perform other actions upon successful login
      } catch (error) {
        console.error("Error logging in:", error.response.data.message);
      }
    }
  };

  return (
    <Body>
      <h1>Login</h1>
      <Form onSubmit={onSubmit}>
        <InputField
          name="username"
          label="Username or email address"
          value={formData.username}
          onChange={handleChange}
          error={formErrors.username}
        />
        <InputField
          name="password"
          label="Password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          error={formErrors.password}
        />
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </Body>
  );
}
