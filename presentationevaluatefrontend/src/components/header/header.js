import React from "react";
import logo from "../../images/pewhite.png";
import './header.css'
const Header = () => {
  return (
    
      <div className="header">
        <div className="Logo">
          <img src={logo} className="LogoImage" alt="Logo" />
          <p className="LogoTitle h3 text-black fw-bold">
            Presentation Evaluator
          </p>
        </div>
        <div className="MenuOptionGroup">
          <p className="MenuOption">Explore</p>
          <p className="MenuOption">About Us</p>
          <p className="MenuOption">Contact Us</p>
        </div>
      </div>
    
  );
};

export default Header;
