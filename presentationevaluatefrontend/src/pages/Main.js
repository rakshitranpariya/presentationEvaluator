import { useState } from "react";
import "./Main.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Header from '../components/header/header'
import Footer from '../components/footer/footer'
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
    
          <Header />
         
       
            <main>
              <form onSubmit={handleSubmit}>
                <h1 class="Heading">React File Upload</h1>
                <input type="file" onChange={handleFileChange} />
                <button type="submit" class="btn btn-primary">
                  Upload
                </button>
              </form>
            </main>
         
           <Footer/>
         
    </div>
  );
};
export default Main;
