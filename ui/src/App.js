import React from 'react';
import {
  QueryClient,
  QueryClientProvider
} from "react-query";
import { Route, Routes } from "react-router-dom";
import "./App.css";
import About from './pages/About';
import HostAccess from './pages/HostAccess';

function App() {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route path="/" element={<HostAccess />} />
        <Route path="about" element={<About />} />
      </Routes>
    </QueryClientProvider>
  );
}

export default App;
