import { useState } from "react";
import "./Main.css";
import "bootstrap/dist/css/bootstrap.min.css";
import logo from "../images/pewhite.png"; // Adjust the path according to your project structure
const Main = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
          enctype: "multipart/form-data",
        });

        const result = await response.json();
        console.log("Success:", result);
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      console.log("No file selected");
    }
  };

  return (
    <div className="MainBody">
    
            <header>
              <div className="Logo">
                <img src={logo} className="LogoImage" alt="Logo"></img>
                <p className="LogoTitle h3 text-black fw-bold">
                  {" "}
                  Presentation Evaluator{" "}
                </p>
              </div>
              <div class="MenuOptionGroup">
                <p class="MenuOption">Explore</p>
                <p class="MenuOption">About Us</p>
                <p class="MenuOption"> Contact Us </p>
              </div>
            </header>
         
       
            <main>
              <form onSubmit={handleSubmit}>
                <h1 class="Heading">React File Upload</h1>
                <input type="file" onChange={handleFileChange} />
                <button type="submit" class="btn btn-primary">
                  Upload
                </button>
              </form>
            </main>
         
            <footer>
              <p class="FooterText">All rights reserved.</p>
            </footer>
         
    </div>
  );
};
export default Main;
