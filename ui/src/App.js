import React from 'react';
import { Routes, Route } from "react-router-dom";
import "./App.css";
import About from './pages/About';
import Home from './pages/Home';

function App() {
  return (
    <div className="m-0 w-full h-full bg-black overflow-x-scroll text-gray-400" >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
        </Routes>
    </div>
  );
}

export default App;
