
import React, { useMemo } from 'react';
import { useTable } from 'react-table';
import TableLayout from './TableLayout';

export default function TableInstance({columnData, tableData}){
  
  const [columns, data] = useMemo(
    () => {
      const columns = [
        {
          Header: 'Team',
          accessor: 'team_name',
          Cell: (props) => {
            console.log(props);
            return <div>{props}</div>;
          },
        }
      ];
      for(let service of columnData){
        columns.push(
          {
            Header: service.sg_name,
            accessor: service.sg_key
          }
        );
      }
      return [columns, tableData];
    },
    [columnData, tableData]
  );
    
  // const [data] = useMemo(
  //   () => {
  //     return [tableData];
  //   },
  //   [tableData]
  // );

  const tableInstance = useTable({ columns, data });

  return (
    <TableLayout {...tableInstance} />
  );
}