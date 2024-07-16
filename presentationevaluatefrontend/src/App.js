import './App.css';
import { BrowserRouter, Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import Home from './pages/Home';
import PptUploader from './pages/PptUploader';
import PresentationRecorder from './pages/PresentationRecorder';

function App() {
  return (
    <BrowserRouter>
  <Routes>
    <Route  path="/" element={<Home/>} />
    <Route  path="/uploadppt" element={<PptUploader/>} />
    <Route  path="/PresentationRecorder" element={<PresentationRecorder/>} />
  </Routes>
  </BrowserRouter>

  );
}

export default App;
