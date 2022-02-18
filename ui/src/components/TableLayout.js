
import _ from "lodash";

export default function TableLayout({
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  }
){
return (
        <table {...getTableProps()}>
            <thead>
                {headerGroups.map(headerGroup => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                    {headerGroup.headers.map(column => (
                    <th {...column.getHeaderProps()}>{column.render('Header')}</th>
                    ))}
                </tr>
                ))}
            </thead>
            <tbody {...getTableBodyProps()}>
                 {rows.map((row, i) => {
                     prepareRow(row);
                     return (
                        <tr {...row.getRowProps()} className="text-xs">
                            
                            {_.map(row.values, (value) => {
                                if(typeof value === "string"){
                                    return <td className="w-4 h-4 truncate overflow-hidden">{value}</td>
                                }
                                else{
                                    return <td className="w-20 h-4">
                                        <div className="p-1 bg-red-800 text-white">
                                            {value.ip}
                                        </div>
                                    </td>
                                }
                            })}
                        </tr>
                     )
                 })}
            </tbody>
        </table>
    );
};