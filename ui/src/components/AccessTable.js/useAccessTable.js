import React from 'react';
import { mockHighLevelAcessData } from "../../fixtures/utils";

export default function useAccessTable(){
    let data = mockHighLevelAcessData(20,15,10);
    let rowData = data.data;
    let teams = data.teamList;

    function getColumns(teams) {
        let columns = [{
            Header: "Services",
            accessor: "service_group"
        }];
        // if (teams) {
        //     for(let team of teams){
        //         columns.push(
        //             {
        //                 Header: team,
        //                 accessor: team
        //             }
        //         );
        //     }
        // }
        return columns;
    }

    const tableColumns = React.useMemo(() => [
        getColumns(teams)
      ],
      [teams]
    );

    const tableData = React.useMemo(() => [
        rowData
      ], [rowData]
      ) 

  
    let isLoading = false;

  
    if (isLoading || !data) {
      return <div>Loading...</div>
    }
  
    return {
        tableColumns,
        tableData
    };
};