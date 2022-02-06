import { ThemeProvider } from '@emotion/react';
import { Button, createTheme } from '@mui/material';
import React, { useState } from 'react';
import { Routes, Route } from "react-router-dom";
import "./App.css";
import About from './pages/About';
import Home from './pages/Home';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const backgroundColor = darkMode ? '#292929' : '#FFFFFF';
  const theme = createTheme(  {
    palette: {
    mode: darkMode ? 'dark' : 'light',
  }
  });
  return (
    <div className="App" style={{backgroundColor: backgroundColor, width:'100vw', height:'100vh'}}>
      <ThemeProvider theme={theme}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
        </Routes>
      </ThemeProvider>
    </div>
  );
}

export default App;
