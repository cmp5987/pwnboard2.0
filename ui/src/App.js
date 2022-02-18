import React from 'react';
import { Routes, Route } from "react-router-dom";
import "./App.css";
import About from './pages/About';
import Home from './pages/Home';

function App() {
  return (
    <div className="App" >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
        </Routes>
    </div>
  );
}

export default App;
