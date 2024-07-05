import './App.css';
import { BrowserRouter, Routes } from 'react-router-dom';
import { Route } from 'react-router-dom';
import Home from './pages/Home';
import Main from './pages/Main';

function App() {
  return (
    <BrowserRouter>
  <Routes>
    {/* <Route  path="/" element={<Home/>} /> */}
    <Route exact path="/main" element={<Main/>} />
  </Routes>
  </BrowserRouter>

  );
}

export default App;
