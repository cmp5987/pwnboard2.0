import { useEffect, useState } from "react";
import { testDataSample1 } from "../fixtures/testDataSample1";
import { mockHighLevelAcessData } from "../fixtures/utils";
import TableInstance from "./TableInstance";

export default function TableQuery(){
  let testData = mockHighLevelAcessData(20,20,10);
  console.log(testData)

  function formatData(inData){
    let formattedData = [];

    for(let row of inData){
      formattedData.push(
        {
          "service_group": row.service_group, ...row.teams
        }
      )
    }
    return formattedData
  }
  let formattedData = formatData(testData.data);
  let teamData = Object.keys(testDataSample1[0].teams);
  
    return (
      <TableInstance columnData={testData.teamList} tableData={formattedData}/>
    );
};