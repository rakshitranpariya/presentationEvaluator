import { useState } from "react";
const Main = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);  
    };

    const handleSubmit = async (event) => {
        event.preventDefault();  
        if (file) {
            const formData = new FormData();
            formData.append('file', file);  

            try {
                const response = await fetch('http://localhost:5000/upload', {
                    method: 'POST',
                    body: formData,
                    enctype:"multipart/form-data"
                });

                const result = await response.json();
                console.log('Success:', result);
            } catch (error) {
                console.error('Error:', error);
            }
        } else {
            console.log('No file selected');
        }
    };

    return (
        <div>
            <h1>Hey This is Main Page</h1>
            <form onSubmit={handleSubmit}>
                <h1>React File Upload</h1>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
        </div>
       
    );
}
export default Main;