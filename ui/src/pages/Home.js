import * as React from "react";
import { Link } from "react-router-dom";
import AccessTable from "../components/AccessTable.js/AccessTable";
import BoardTable from "../components/BoardTable";
import TableQuery from "../components/TableQuery";
import { testDataSample1 } from "../fixtures/testDataSample1";
import { mockHighLevelAcessData } from "../fixtures/utils";



function Home() {
  return (
    <div className="">
      <main>
        <h2>Welcome to the homepage!</h2>
        <p>You can do this, I believe in you.</p>
        <TableQuery />
        {/* <AccessTable /> */}
      </main>
      <nav>
        <Link to="/about">About</Link>
      </nav>
    </div>
  );
}
export default Home;
  