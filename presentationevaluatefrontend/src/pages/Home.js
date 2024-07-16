import React from "react";
import "./Home.css";
import "./global.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from '../components/header/header';
import Footer from '../components/footer/footer';
const Home = () => {
    const redirect = () => {
        window.location.href = '/uploadppt'; 
      };
    return (
        <div class="HomeBody background">
            <Header />
            <div className="MainBanner" >
                <div class="ButtonDiv">
                    <button className="btn btn-dark BannerButtons fw-bolder" onClick={redirect}>Start Evaluating</button>
                    <button className="btn btn-outline-dark BannerButtons fw-bolder"> About Us</button>
                </div>
            </div>
         <Footer />
        </div>        
    );
}
export default Home;