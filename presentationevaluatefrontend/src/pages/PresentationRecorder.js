import React, { useState, useEffect, useRef } from "react";
import "./PresentationRecorder.css";
import "./global.css";
import Header from "../components/header/header";
import Footer from "../components/footer/footer";
import Webcam from "react-webcam";

const PresentationRecorder = () => {
  const [count, setCount] = useState(0); // Total number of images
  const [currentImageIndex, setCurrentImageIndex] = useState(0); // Index of the current image
  const [currentImage, setCurrentImage] = useState(null); // URL of the current image
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  // const [recordedChunks, setRecordedChunks] = useState([]);
  const recordedChunksRef = useRef([]);
  const webcamRef = useRef(null);
  
  useEffect(() => {
    const fetchImageCount = async () => {
      try {
        const response = await fetch("http://localhost:5000/slide/count");
        if (!response.ok) {
          throw new Error("Failed to fetch image count");
        }
        const data = await response.json();
        setCount(data.count);
      } catch (error) {
        console.error("Error fetching image count:", error);
      }
    };
    
    fetchImageCount();
  }, []);
  
  useEffect(() => {
    const fetchImage = async (index) => {
      try {
        const response = await fetch(`http://localhost:5000/slide/${index}`);
        if (!response.ok) {
          throw new Error("Failed to fetch image");
        }
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setCurrentImage(imageUrl);
      } catch (error) {
        console.error("Error fetching image:", error);
      }
    };
    
    if (count > 0) {
      fetchImage(currentImageIndex);
    }
  }, [currentImageIndex, count]);
  
  const nextImage = () => {
    setCurrentImageIndex((prevIndex) =>
      prevIndex === count - 1 ? 0 : prevIndex + 1
  );
};

const prevImage = () => {
  setCurrentImageIndex((prevIndex) =>
    prevIndex === 0 ? count - 1 : prevIndex - 1
);
};

const startRecording = () => {
  if (webcamRef.current && webcamRef.current.video) {
    console.log("Webcam video element found:", webcamRef.current.video);
    const stream = webcamRef.current.video.srcObject;
    const options = { mimeType: "video/webm; codecs=vp9" };
    const recorder = new MediaRecorder(stream, options);
    
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        console.log("🚀 ~ startRecording ~ event.data:", event.data)
        recordedChunksRef.current.push(event.data);
        // console.log("🚀 ~ PresentationRecorder ~ recordedChunks:", recordedChunks)
        }
      };
      
      recorder.onstop = async () => {
        // console.log("Recorder stopped. Recorded chunks:", recordedChunks);
        const blob = new Blob(recordedChunksRef.current, { type: "video/webm" });
        const videoName = `${currentImageIndex}_${new Date()
          .toISOString()
          .replace(/[:.-]/g, "_")}.webm`;
        const formData = new FormData();
        // console.log("Type of elements in recordedChunks:", typeof recordedChunks[0]);
        formData.append("video", blob ,videoName);
        
        try {
          const response = await fetch("http://localhost:5000/upload_video", {
            method: "POST",
            'Content-Type': 'multipart/form-data',
            body: formData,
          });
          if (!response.ok) {
            throw new Error("Failed to upload and convert video");
          }
          console.log("Video uploaded successfully");
        } catch (error) {
          console.error("Error uploading and converting video:", error);
        } finally {
          // Clear recorded chunks after uploading
          recordedChunksRef.current = [];
        }
      };
      
      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
    } else {
      console.log("Webcam video element not found");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="containerbody background">
      <Header />
      <div className="container">
        <div className="row ">
          <div className="col-lg-8 col-12 presentationDisplaySession">
            <div
              id="carouselExampleControls"
              className="carousel slide"
              data-interval="false"
            >
              <div className="carousel-inner">
                <div className="carousel-item active">
                  <img
                    className="d-block w-100 img-class"
                    src={currentImage}
                    alt="Current slide"
                  />
                </div>
              </div>
              {currentImageIndex !== 0 && (
                <a
                  className="carousel-control-prev"
                  href="#carouselExampleControls"
                  role="button"
                  data-slide="prev"
                  onClick={prevImage}
                >
                  <span
                    className="carousel-control-prev-icon"
                    aria-hidden="true"
                  ></span>
                  <span className="sr-only">Previous</span>
                </a>
              )}
              {currentImageIndex !== count - 1 && (
                <a
                  className="carousel-control-next"
                  href="#carouselExampleControls"
                  role="button"
                  data-slide="next"
                  onClick={nextImage}
                >
                  <span
                    className="carousel-control-next-icon"
                    aria-hidden="true"
                  ></span>
                  <span className="sr-only">Next</span>
                </a>
              )}
            </div>
            <div className="buttonsSection">
              <button
                className="btn btn-primary buttons"
                onClick={startRecording}
                disabled={isRecording}
              >
                Start
              </button>
              <button
                className="btn btn-primary buttons"
                onClick={stopRecording}
                disabled={!isRecording}
              >
                Stop
              </button>
            </div>
          </div>

          <div className="col-lg-4 col-12">
            <Webcam
              className="webcam-feed"
              ref={webcamRef}
              audio={true}
              videoConstraints={{
                width: 1280,
                height: 720,
                facingMode: "user",
              }}
            />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default PresentationRecorder;
