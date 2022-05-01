
import React, { useMemo } from 'react';
import { useTable } from 'react-table';
import TableLayout from '../TableLayout';
import useAccessTable from './useAccessTable';

export default function AccessTable(){
    const {
        columnData,
        tableData
    } = useAccessTable();
//     console.log(tableColumns);
//     console.log(tableData);
//     let data = [];

//    const tableInstance = useTable({ tableColumns, data });
//    console.log(tableInstance)

    const [columns, data] = useMemo(
    () => {
      const columns = [
        {
          Header: 'Service',
          accessor: 'service_group',
          Cell: (props) => {
            console.log(props);
            return <div>{props}</div>;
          },
        }
      ];
    //   for(let service of columnData){
    //     columns.push(
    //       {
    //         Header: service.sg_name,
    //         accessor: service.sg_key
    //       }
    //     );
    //   }
      return [columns, tableData];
    },
    [columnData, tableData]
  );

  const tableInstance = useTable({ columns, data });

  return (
      <div>Testing</div>
    //  <TableLayout {...tableInstance} />
  );
}