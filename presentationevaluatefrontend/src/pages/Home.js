import React from "react";
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import logo from '../images/logo.png'; // Adjust the path according to your project structure

const Home = () => {
    return (
        <div>
            <div className="header">
                <img src={logo} className="Logo" alt="Logo"></img>
                <p className="LogoTitle"> presentrationelvcatu</p>
                </div>
                <button className="primaryButton"></button>
                <button className="LoginIn"></button>
        </div>
        
    );
}
export default Home;