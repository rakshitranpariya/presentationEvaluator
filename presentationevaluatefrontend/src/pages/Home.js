import React from "react";
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import logo from '../images/pewhite.png'; // Adjust the path according to your project structure

const Home = () => {
    return (
        <div class="HomeBody">
            <div className="header">
                <div className="Logo">
                    <img src={logo} className="LogoImage" alt="Logo"></img>
                    <p className="LogoTitle h3 text-black fw-bold"> Presentation Evaluator </p>
                </div>
                <div class="LeftOptions">
                    <p class="MenuOption">Explore</p>
                    <p class="MenuOption">About Us</p>
                    <p class="MenuOption"> Contact Us </p>
                </div>
            </div>
            <div className="MainBanner">
                <div class="ButtonDiv">
                    <button className="btn btn-dark BannerButtons ">Start Evaluating</button>
                    <button className="btn btn-outline-dark BannerButtons"> About Us</button>
                </div>
            </div>
                
            <div class="Footer">
                    <p class="FooterText">All rights reserved.</p>
            </div>
             

        </div>
        
    );
}
export default Home;