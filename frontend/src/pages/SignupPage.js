import React, { useState } from "react";
import axios from 'axios';

const baseurl = "http://localhost:5000"
function Signup() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");


    const handleSignup = async () => {
        try {
            const response = await axios.post(`${baseurl}/signup`, {
               username,
               email,
               password, 
            });
            console.log(response.data.message)
        } catch (error) {
            console.error("Error signing up:", error.response.data.message);
        }
    };
    
    return (
        <div>
            <h2>Signup</h2>
            <form>
                <input 
                    type="text" 
                    placeholder="Username" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input 
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input 
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={handleSignup}>Sign Up</button>
            </form>
        </div>
    );
};

export default Signup;