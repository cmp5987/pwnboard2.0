import React from 'react';
import { Route, Routes } from "react-router-dom";
import "./App.css";
import About from './pages/About';
import HostAccess from './pages/HostAccess';

function App() {
  return (
      <Routes>
        <Route path="/" element={<HostAccess />} />
        <Route path="about" element={<About />} />
      </Routes>
  );
}

export default App;
