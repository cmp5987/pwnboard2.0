
import _ from "lodash";
import HostTableCell from "./HostTableCell/HostTableCell";

export default function TableLayout({
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  }
){
return (
        <table {...getTableProps()} className="">
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
                                    return <td className="w-4 h-4 truncate overflow-hidden" key={`service_${value}`}>{value}</td>
                                }
                                else {
                                    // let minIsZero = _.random(0, 20) < 1 ? 0 : value.tools.length - 1;
                                    // let randomCurrentAccess = _.random(minIsZero, value.tools.length);
                                    // let accessColor = randomCurrentAccess === value.tools.length ? "bg-green-900/50" : randomCurrentAccess === 0 ? "bg-red-900/25" : randomCurrentAccess < 3 ? "bg-red-700" : "bg-red-700/50";
                                    // return <td className="p-1 " key={`host_${value.primary_ip}`}>
                                    //     <div className={`p-1 text-neutral-300 flex flex-col gap-1 rounded shadow-sm items-center hover:cursor-pointer hover:bg-neutral-700 hover:shadow-md ${accessColor}`} onClick={ ()=> console.log(value)} tabIndex={0}>
                                    //         <div className="font-medium">
                                    //             {value.primary_ip}
                                    //         </div>
                                    //         <div className={`w-full rounded flex flex-row justify-center`}>
                                    //             <span>
                                    //                 {randomCurrentAccess} / {value.tools.length}
                                    //             </span>
                                    //         </div>
                                    //     </div>
                                    // </td>
                                    return <td className="p-1 " key={`host_${value.primary_ip}`}><HostTableCell  cellData={value}/></td>
                                }
                            })}
                        </tr>
                     )
                 })}
            </tbody>
        </table>
    );
};