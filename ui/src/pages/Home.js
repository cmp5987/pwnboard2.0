import { Typography } from "@mui/material";
import * as React from "react";
import { Link } from "react-router-dom";
import AccessDataGrid from "../components/AccessDataGrid";
import AccessGrid from "../components/AccessGrid";
import NavBar from "../components/NavBar";

function Home() {
  return (
    <>
      <main>
        <NavBar />
        <AccessDataGrid />
      </main>
      {/* <nav>
        <Link to="/about">About</Link>
      </nav> */}
    </>
  );
}
export default Home;
  