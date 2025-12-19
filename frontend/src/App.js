import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Loading from './pages/Loading';
import Resultado from './pages/Resultado';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/loading" element={<Loading />} />
          <Route path="/resultado" element={<Resultado />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;