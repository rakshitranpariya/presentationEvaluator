import React, { useState, useEffect } from "react";
import { Doughnut } from "react-chartjs-2";
import "./global.css";
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from "chart.js";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faMinus } from "@fortawesome/free-solid-svg-icons";
import './ResultPage.css'; 

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const ResultPage = () => {
    const [scoresList, setScoresList] = useState([]);
    const [error, setError] = useState(null);
    const [expandedSlides, setExpandedSlides] = useState([]); 
    const [images, setImages] = useState({});

    useEffect(() => {
        const fetchAllScores = async () => {
            try {
                const response = await fetch('http://localhost:5000/get_all_scores', { method: "POST" });
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const data = await response.json();
                setScoresList(data);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchAllScores();
    }, []);

    const fetchImage = async (index) => {
        try {
            const response = await fetch(`http://localhost:5000/slide/${index}`);
            if (!response.ok) {
                throw new Error("Failed to fetch image");
            }
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            setImages(prev => ({ ...prev, [index]: imageUrl }));
        } catch (error) {
            console.error("Error fetching image:", error);
        }
    };

    useEffect(() => {
        scoresList.forEach(scores => {
            fetchImage(scores.slide_id);
        });
    }, [scoresList]);

    const handleDownloadPresentation = async () => {
        try {
            const response = await fetch('http://localhost:5000/combine_videos', {
                method: 'POST',
                responseType: 'blob',
            });

            if (!response.ok) {
                throw new Error(`Failed to download video: ${response.statusText}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'combined_video.mp4'; // Filename for the downloaded file
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (error) {
            console.error('Error downloading the presentation:', error);
        }
    };

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (scoresList.length === 0) {
        return (
            <div className="spinner-container">
                <div className="spinner-grow text-primary" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
                <div>Please Wait for 4-5 Minutes.</div>
            </div>
        );
    }

    const sortedScoresList = [...scoresList].sort((a, b) => a.slide_id - b.slide_id);

    const createChartData = (label, value) => {
        const color = value >= 33 ? '#4CAF50' : '#FF6384'; // Green if score >= 33, Red if score < 33

        return {
            labels: [label],
            datasets: [
                {
                    data: [value, 100 - value],
                    backgroundColor: [color, '#e0e0e0'],
                    borderColor: '#fff',
                    borderWidth: 2,
                }
            ]
        };
    };

    const handleSlideClick = (slideId) => {
        setExpandedSlides(prev => 
            prev.includes(slideId) ? prev.filter(id => id !== slideId) : [...prev, slideId]
        );
    };

    return (
        <div className="background">
            <div className="header-container">
                <h2 className="text-black p-3 border-primary">
                    Results for All Slides
                </h2>
                <button onClick={handleDownloadPresentation} className="btn btn-primary download-button">
                    Download Presentation
                </button>
            </div>
            {sortedScoresList.map((scores) => (
                <div key={scores.slide_id} className="slide_border">
                    <div className='total_title'>
                        <h3
                            onClick={() => handleSlideClick(scores.slide_id)}
                            className={`slide-title ${expandedSlides.includes(scores.slide_id) ? 'expanded' : ''}`}
                        >
                            Slide {scores.slide_id}
                            <FontAwesomeIcon
                                icon={expandedSlides.includes(scores.slide_id) ? faMinus : faPlus}
                                className={`toggle-icon ${expandedSlides.includes(scores.slide_id) ? 'expanded' : ''}`}
                            />
                        </h3>
                        
                        <div className="GoodSection">
                            {scores.content_coverage >= 33 && (
                                <div className="bubble small">Content Coverage</div>
                            )}
                            {scores.correctness >= 33 && (
                                <div className="bubble small">Correctness</div>
                            )}
                            {scores.consistency_in_words >= 33 && (
                                <div className="bubble small">Consistency in Words</div>
                            )}
                            {scores.textual_cohesion >= 33 && (
                                <div className="bubble small">Textual Cohesion</div>
                            )}
                            {scores.language_and_grammar >= 33 && (
                                <div className="bubble small">Language and Grammar</div>
                            )}
                        </div>
                        <div className="Warningtab">
                            {scores.content_coverage < 33 && (
                                <div className="bubble small">Content Coverage</div>
                            )}
                            {scores.correctness < 33 && (
                                <div className="bubble small">Correctness</div>
                            )}
                            {scores.consistency_in_words < 33 && (
                                <div className="bubble small">Consistency in Words</div>
                            )}
                            {scores.textual_cohesion < 33 && (
                                <div className="bubble small">Textual Cohesion</div>
                            )}
                            {scores.language_and_grammar < 33 && (
                                <div className="bubble small">Language and Grammar</div>
                            )}
                        </div>
                        {images[scores.slide_id] && (
                            <img src={images[scores.slide_id]} alt={`Slide ${scores.slide_id}`} className="slide-image" />
                        )}
                    </div>
                    {expandedSlides.includes(scores.slide_id) && (
                        <div className="chart-container" style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', alignItems:'center', justifyContent: 'center', padding:"15px"}}>
                            <div>
                                <Doughnut
                                    data={createChartData('Content Coverage', scores.content_coverage)}
                                    options={{ responsive: true }}
                                    style={{ width: '200px', height: '200px', margin: '0px 0px 5px 5px' }}
                                />
                            </div>
                            <div>
                                <Doughnut
                                    data={createChartData('Correctness', scores.correctness)}
                                    options={{ responsive: true }}
                                    style={{ width: '200px', height: '200px' }}
                                />
                            </div>
                            <div>
                                <Doughnut
                                    data={createChartData('Consistency in Words', scores.consistency_in_words)}
                                    options={{ responsive: true }}
                                    style={{ width: '200px', height: '200px' }}
                                />
                            </div>
                            <div>
                                <Doughnut
                                    data={createChartData('Textual Cohesion', scores.textual_cohesion)}
                                    options={{ responsive: true }}
                                    style={{ width: '200px', height: '200px' }}
                                />
                            </div>
                            <div>
                                <Doughnut
                                    data={createChartData('Language and Grammar', scores.language_and_grammar)}
                                    options={{ responsive: true }}
                                    style={{ width: '200px', height: '200px' }}
                                />
                            </div>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default ResultPage;
