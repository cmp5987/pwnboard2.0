import { Box, Card, CardContent, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import * as React from "react";
import { red, purple, blue, grey } from '@mui/material/colors';

function AccessCard({accessDetails}) {
    let accessPercent = accessDetails.currentAccess / accessDetails.totalAccess;
    let accessColor = accessPercent > .50 ? red[900] : accessPercent === 0 ? blue[700] : grey[800]; 
    return (
        <Card width={100} sx={{ display: 'flex', flexDirection:"row", flexGrow:'1'}}>
            <Box sx={{ display: 'flex', flexShirnk:'0', flexDirection: 'column', backgroundColor: accessColor, justifyContent:'center', alignItems:'center', minheight: '25vh'}}>
                <CardContent>
                    <Typography component="div" variant="subtitle2" color="common.white" noWrap="true" >
                       {accessDetails.currentAccess} / {accessDetails.totalAccess}
                    </Typography>
                </CardContent>        
            </Box>
            <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', justifyItems: 'flex-start' }}>
                <CardContent>
                    <Typography component="div" variant="subtitle1">
                        {accessDetails.ip}
                    </Typography>
                    <Typography component="div" variant="body2" color={grey[500]}>
                        {accessDetails.team}
                    </Typography>
                </CardContent>
            </Box>
        </Card>
    );
}
export default AccessCard;
  