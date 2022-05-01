
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
                        <tr {...row.getRowProps()} className="text-sm">
                            
                            {_.map(row.values, (value) => {
                                if(typeof value === "string"){
                                    return <td className="w-4 h-4 truncate overflow-hidden">{value}</td>
                                }
                                else{
                                    return <td className="h-4">
                                        <div className="p-1 bg-red-800 text-white">
                                            <div>
                                                {value.primary_ip}
                                            </div>
                                            <div className="flex flex-row flex-wrap gap-1">
                                                <span>
                                                    {value.tools.length -1} / {value.tools.length}
                                                </span>
                                                <span>
                                                    Callbacks 
                                                </span>
                                            </div>
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