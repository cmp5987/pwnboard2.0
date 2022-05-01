
import React, { useMemo } from 'react';
import { useTable } from 'react-table';
import TableLayout from './TableLayout';

export default function TableInstance({columnData, tableData}){
  
  const [columns, data] = useMemo(
    () => {
      const columns = [
        {
          Header: 'Service',
          accessor: 'service_group',
        }
      ];
      for(let team of columnData){
        columns.push(
          {
            Header: team,
            accessor: team
          }
        );
      }
      return [columns, tableData];
    },
    [columnData, tableData]
  );

  const tableInstance = useTable({ columns, data });

  return (
    <TableLayout {...tableInstance} />
  );
}