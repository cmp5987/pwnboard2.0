import { Box } from "@mui/material";
import * as React from "react";
import AccessCard from "./AccessCard";
import _ from "lodash";
import { faker } from 'https://cdn.skypack.dev/@faker-js/faker';

function AccessGrid({accessDetails}) {
    let totalAccess = _.random(1,10);
    const accessArray = [{
        ip: '19.0.10.10',
        totalAccess: 5,
        currentAccess: 10,
        team: "Team 1",
        service: "Kali"
    },{
        ip: '255.0.10.10',
        totalAccess: 5,
        currentAccess: 10,
        team: "Team 2",
        service: "db"
    },{
        ip: '100.0.10.10',
        totalAccess: 5,
        currentAccess: 10,
        team: "Team 3",
        service: "Kali"
    },{
        ip: '10.0.9.9',
        totalAccess: 5,
        currentAccess: 10,
        team: "Team 4",
        service: "Win 8"
    }]
    return (
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(10, 200px)',  width:'100%', gap: 2 }}>
            {accessArray.map((item,i) => {
                return <AccessCard  key={i} accessDetails={item} />
            })}
        </Box>
    );
}
export default AccessGrid;
  