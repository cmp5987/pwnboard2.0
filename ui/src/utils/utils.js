import _ from "lodash";
import { serviceList } from "./consts";
import { faker } from 'https://cdn.skypack.dev/@faker-js/faker';

function mockServiceAccessData(team){
    let mockArray = {};
    for(let value of serviceList){
        let totalAccess = _.random(1,10);
        mockArray[value] = {
            ip: faker.internet.ip(),
            team: team,
            totalAccess: totalAccess,
            currentAccess: _.random(0, totalAccess)
        };      
    }
    return mockArray;
}

export function mockHighLevelAcessData(teamCount){

    let mockTeamArray = [];

    for(let index = 0; index < teamCount; index++){
        let team = "Team " + index; 
        let mockServiceObject = mockServiceAccessData(team);
        mockTeamArray.push(
            {
                id: index,
                team: team,
                ...mockServiceObject
            }
        )
    }

    console.log(mockTeamArray);
    return mockTeamArray;
}

