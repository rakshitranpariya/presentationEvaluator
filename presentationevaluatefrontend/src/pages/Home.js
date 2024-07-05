import React from "react";
import "./Home.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import logo from '../images/pewhite.png'; // Adjust the path according to your project structure
import Header from '../components/header/header';
import Footer from '../components/footer/footer';
const Home = () => {
    return (
        <div class="HomeBody">
            <Header />
            <div className="MainBanner">
                <div class="ButtonDiv">
                    <button className="btn btn-dark BannerButtons ">Start Evaluating</button>
                    <button className="btn btn-outline-dark BannerButtons"> About Us</button>
                </div>
            </div>
                
         <Footer />
             
        </div>
        
    );
}
export default Home;