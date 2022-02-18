import * as React from "react";
import { Link } from "react-router-dom";
import BoardTable from "../components/BoardTable";
import TableQuery from "../components/TableQuery";



function Home() {
  return (
    <>
      <main>
        <h2>Welcome to the homepage!</h2>
        <p>You can do this, I believe in you.</p>
        <TableQuery />
      </main>
      <nav>
        <Link to="/about">About</Link>
      </nav>
    </>
  );
}
export default Home;
  