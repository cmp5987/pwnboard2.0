import _ from "lodash";
import { faker } from 'https://cdn.skypack.dev/@faker-js/faker';

function mockTeamList(teamCount){
    let teams = [];
    for(let index = 0; index < teamCount; index++){
        teams.push( {
            'team_name': faker.company.companySuffix(),
            'team_key': faker.company.companySuffix(),
            'team_id': faker.datatype.uuid()
        });
    }
    return teams;
}

function mockServiceList(serviceCount){
    let services = [];
    for(let index = 0; index < serviceCount; index++){
        services.push(
            {
                "sg_key": faker.datatype.uuid(),            
                "sg_name": faker.commerce.product(),
                "sg_id": faker.datatype.uuid()
            },
        );
    }
    return services;
}


export function mockHighLevelAcessData(teamCount, serviceCount){

    let mockTeamArray = mockTeamList(teamCount);
    let mockServiceArray = mockServiceList(serviceCount);
    let mockBoardData = [];

    for(let team of mockTeamArray){
        let mockRowData = {
            "team_name": team.team_name,
        };
        for(let service of mockServiceArray){
            let totalAccess = _.random(1,10);
            mockRowData[service.sg_key] =
                {
                    "unsanitized_name": service.sg_name,
                    "ip": faker.internet.ip(),
                    "total_access": totalAccess,
                    "current_access": _.random(0, totalAccess)
                };
        }
        mockBoardData.push(mockRowData);
    }
    return {"teamList": mockTeamArray, 'serviceList': mockServiceArray, 'data': mockBoardData };
}

