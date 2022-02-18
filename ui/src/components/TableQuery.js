import { useEffect, useState } from "react";
import { mockHighLevelAcessData } from "../utils/utils";
import TableInstance from "./TableInstance";

export default function TableQuery(){
  
    const [tableData, setTableData] = useState(null);
    const mockData = mockHighLevelAcessData(10,15);

    console.log(mockData.data);
  
    let isLoading = false;
  
    useEffect(() => {
      setTableData(
          [
            {
            "id": 1,
            "name": "How to use react-table in reporting dashboard",
            "active": 40,
            "status": "locked",
            "upvotes": 30
            },
            {
            "id": 2,
            "name": "How to use react-query for BI solution",
            "active": 31,
            "status": "resolved",
            "upvotes": 39
            }
          ]
      );
    }, []);
  
    if (isLoading || !tableData) {
      return <div>Loading...</div>
    }
  
    return (
      <TableInstance columnData={mockData.serviceList} tableData={mockData.data}/>
    );
};