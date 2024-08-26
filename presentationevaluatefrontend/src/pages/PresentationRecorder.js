import React, { useState, useEffect, useRef } from "react";
import "./PresentationRecorder.css";
import "./global.css";
import Header from "../components/header/header";
import Footer from "../components/footer/footer";
import Webcam from "react-webcam";
import { useNavigate } from 'react-router-dom';

const PresentationRecorder = () => {
  const [count, setCount] = useState(0);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [currentImage, setCurrentImage] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const recordedChunksRef = useRef([]);
  const webcamRef = useRef(null);
  const [recordingStarted, setRecordingStarted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false); // State for spinner
  const navigate = useNavigate();

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

  const handleRecording = async () => {
    if (mediaRecorder) {
      mediaRecorder.stop();

      mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunksRef.current, { type: "video/webm" });
        const videoName = `${currentImageIndex}_${new Date().toISOString().replace(/[:.-]/g, "_")}.webm`;
        const formData = new FormData();
        formData.append("video", blob, videoName);

        try {
          const response = await fetch("http://localhost:5000/upload_video", {
            method: "POST",
            body: formData,
          });
          if (!response.ok) {
            throw new Error("Failed to upload and convert video");
          }
          console.log("Video uploaded successfully");
        } catch (error) {
          console.error("Error uploading and converting video:", error);
        } finally {
          recordedChunksRef.current = [];
        }
      };
    }

    if (currentImageIndex < count - 1) {
      setCurrentImageIndex((prevIndex) => prevIndex + 1);
      startRecording();
    } else {
      setIsRecording(false);
    }
  };

  const startRecording = () => {
    if (webcamRef.current && webcamRef.current.video) {
      const stream = webcamRef.current.video.srcObject;
      const options = { mimeType: "video/webm; codecs=vp9" };
      const recorder = new MediaRecorder(stream, options);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunksRef.current.push(event.data);
        }
      };

      setMediaRecorder(recorder);
      recorder.start();
      setIsRecording(true);
      setRecordingStarted(true);
    } else {
      console.log("Webcam video element not found");
    }
  };

  const submitPresentation = async () => {
    setIsSubmitting(true); // Show spinner

    if (mediaRecorder) {
      mediaRecorder.stop();

      mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunksRef.current, { type: "video/webm" });
        const videoName = `${currentImageIndex}_${new Date().toISOString().replace(/[:.-]/g, "_")}.webm`;
        const formData = new FormData();
        formData.append("video", blob, videoName);

        try {
          const uploadResponse = await fetch("http://localhost:5000/upload_video", {
            method: "POST",
            body: formData,
          });

          if (!uploadResponse.ok) {
            throw new Error("Failed to upload and convert video");
          }
          console.log("Video uploaded successfully");

          const processResponse = await fetch("http://localhost:5000/start_processing", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (!processResponse.ok) {
            throw new Error("Failed to start processing");
          }

          const data = await processResponse.json();
          console.log("Processing started successfully:", data);

          navigate("/ResultPage");
        } catch (error) {
          console.error("Error uploading and processing video:", error);
        } finally {
          recordedChunksRef.current = [];
        }
      };
    }
  };

  return (
    <div className="containerbody background">
      <Header />

      {/* Show spinner when submitting */}
      {isSubmitting ? (
        <div className="spinner-container">
          <div className="spinner-grow text-primary" role="status">
            <span className="sr-only">Loading...</span>
          </div>
          <div>Please Wait for 4-5 Minutes.</div>
        </div>
      ) : (
        <div className="container">
          <div className="row">
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

                {currentImageIndex !== count - 1 && (
                  <a
                    className="carousel-control-next"
                    href="#carouselExampleControls"
                    role="button"
                    data-slide="next"
                    onClick={handleRecording}
                    disabled={!recordingStarted}
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
                {currentImageIndex === 0 && (
                  <button
                    className="btn btn-primary buttons"
                    onClick={startRecording}
                    disabled={isRecording}
                  >
                    Start
                  </button>
                )}
                {currentImageIndex === count - 1 && (
                  <button
                    className="btn btn-primary buttons"
                    onClick={submitPresentation}
                  >
                    Submit
                  </button>
                )}
              </div>
            </div>

            <div className="col-lg-4 col-12 right-container">
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
      )}
      <Footer />
    </div>
  );
};

export default PresentationRecorder;
