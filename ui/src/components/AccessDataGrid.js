import { Box } from '@mui/material';
import Button from '@mui/material/Button';
import { DataGrid } from '@mui/x-data-grid';
import { mockHighLevelAcessData } from '../utils/utils';
import AccessCard from './AccessCard';

const columns = [
    { field: 'id', headerName: '', width: 70 },
    {
        field: 'action',
        headerName: 'ad',
        sortable: false,
        width: 250,
        renderCell: (params) => {
        //   const onClick = (e) => {
        //     e.stopPropagation(); // don't select this row after clicking

        //     const api: GridApi = params.api;
        //     const thisRow: Record<string, GridCellValue> = {};

        //     api
        //       .getAllColumns()
        //       .filter((c) => c.field !== '__check__' && !!c)
        //       .forEach(
        //         (c) => (thisRow[c.field] = params.getValue(params.id, c.field)),
        //       );

        //     return alert(JSON.stringify(thisRow, null, 4));
        //   };

        return <AccessCard />;
        },
    },
    {
        field: 'firstName',
        headerName: 'mail',
        sortable: false,
        width: 250,
        renderCell: (params) => {
        //   const onClick = (e) => {
        //     e.stopPropagation(); // don't select this row after clicking

        //     const api: GridApi = params.api;
        //     const thisRow: Record<string, GridCellValue> = {};

        //     api
        //       .getAllColumns()
        //       .filter((c) => c.field !== '__check__' && !!c)
        //       .forEach(
        //         (c) => (thisRow[c.field] = params.getValue(params.id, c.field)),
        //       );

        //     return alert(JSON.stringify(thisRow, null, 4));
        //   };

        return <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent:'center', alignItems:'center', width: '100%', height: '100%'}}><AccessCard /></Box>;
        },
    },
    {
        field: 'lastName',
        headerName: 'kali',
        sortable: false,
        width: 250,
        renderCell: (params) => {
        //   const onClick = (e) => {
        //     e.stopPropagation(); // don't select this row after clicking

        //     const api: GridApi = params.api;
        //     const thisRow: Record<string, GridCellValue> = {};

        //     api
        //       .getAllColumns()
        //       .filter((c) => c.field !== '__check__' && !!c)
        //       .forEach(
        //         (c) => (thisRow[c.field] = params.getValue(params.id, c.field)),
        //       );

        //     return alert(JSON.stringify(thisRow, null, 4));
        //   };

        return <AccessCard />;
        },
    },
    {
        field: 'parrot',
        headerName: 'kali',
        sortable: false,
        width: 250,
        renderCell: (params) => {
            console.log(params.getValue(params.id, 'parrot'));
        //   const onClick = (e) => {
        //     e.stopPropagation(); // don't select this row after clicking

        //     const api: GridApi = params.api;
        //     const thisRow: Record<string, GridCellValue> = {};

        //     api
        //       .getAllColumns()
        //       .filter((c) => c.field !== '__check__' && !!c)
        //       .forEach(
        //         (c) => (thisRow[c.field] = params.getValue(params.id, c.field)),
        //       );

        //     return alert(JSON.stringify(thisRow, null, 4));
        //   };

        return <AccessCard />;
        },
    },
//   { field: 'firstName', headerName: 'First name', width: 130 },
//   { field: 'lastName', headerName: 'Last name', width: 130 },
//   {
//     field: 'age',
//     headerName: 'Age',
//     type: 'number',
//     width: 90,
//   },
//   {
//     field: 'fullName',
//     headerName: 'Full name',
//     description: 'This column has a value getter and is not sortable.',
//     sortable: false,
//     width: 160,
//     valueGetter: (params) =>
//       `${params.getValue(params.id, 'firstName') || ''} ${
//         params.getValue(params.id, 'lastName') || ''
//       }`,
//   },
];

const rows = [
  { id: 1, lastName: 'Snow', firstName: 'Jon', age: 35, parrot: {ip:'10.0.0.0'} },
  { id: 2, lastName: 'Lannister', firstName: 'Cersei', age: 42, parrot: {ip:'10.0.0.0'} },
  { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 45, parrot: {ip:'10.0.0.0'} },
  { id: 4, lastName: 'Stark', firstName: 'Arya', age: 16, parrot: {ip:'10.0.0.0'} },
  { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null, parrot: {ip:'10.0.0.0'} },
  { id: 6, lastName: 'Melisandre', firstName: null, age: 150, parrot: {ip:'10.0.0.0'} },
  { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44, parrot: {ip:'10.0.0.0'} },
  { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36, parrot: {ip:'10.0.0.0'} },
  { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65, parrot: {ip:'10.0.0.0'} },
  { id: 10, lastName: 'Targaryen', firstName: 'Daenerys', age: null, parrot: {ip:'10.0.0.0'} },
  { id: 11, lastName: 'Melisandre', firstName: null, age: 150, parrot: {ip:'10.0.0.0'} },
  { id: 12, lastName: 'Clifford', firstName: 'Ferrara', age: 44, parrot: {ip:'10.0.0.0'} },
  { id: 13, lastName: 'Frances', firstName: 'Rossini', age: 36, parrot: {ip:'10.0.0.0'} },
  { id: 14, lastName: 'Roxie', firstName: 'Harvey', age: 65, parrot: {ip:'10.0.0.0'} },
];

function formatColumns(data){
    let dataColumnKeys = Object.keys(data[0]);
    let columns = [{ field: 'team', headerName: '', width: 70 }];

    for(let key of dataColumnKeys){
        if(key !== "id" && key !== "team"){
            columns.push(
                {
                    field: key,
                    headerName: key,
                    sortable: false,
                    width: 250,
                    renderCell: (params) => {
                        console.log(params.getValue(params.id, key));
                        return <AccessCard accessDetails={params.getValue(params.id, key)} />;
                    },
                }
            );
        }
    }
    return columns;

}

const data = mockHighLevelAcessData(20);
const formattedColumns = formatColumns(data);

export default function AccessDataGrid() {
  return (
    <div style={{ height:'90vh', width: '100%' }}>
      <DataGrid rowHeight={100} rows={data} columns={formattedColumns} pageSize={20}/>
    </div>
  );
}
