import { testDataSample1 } from "../fixtures/testDataSample1";
import TableInstance from "./TableInstance";

export default function TableQuery({ data }) {
  // const { status, data, error, isFetching } = useBoard();
  // console.log(data);
  // console.log(getBackendBaseUrl());

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
  let formattedData = formatData(data.data);
  let teamData = Object.keys(testDataSample1[0].teams);

    return (
      <TableInstance columnData={data.teamList} tableData={formattedData}/>
    );
};