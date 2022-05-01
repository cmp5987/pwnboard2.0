import _ from "lodash";
import { faker } from 'https://cdn.skypack.dev/@faker-js/faker';

function onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}

function mockTeamList(teamCount){
    let teams = [];
    for(let i = 0; i < teamCount; i++){
      teams.push(faker.name.lastName() + " " + i);
    }
    return teams.filter(onlyUnique);
}
function mockServiceList(serviceCount){
    let services = [];
    for(let i = 0; i < serviceCount; i++){
      services.push(faker.commerce.product() + " " + i);
    }
    return services.filter(onlyUnique);
}
function mockToolList(toolCount){
    let tools = [];
    for(let i = 0; i < toolCount; i++){
      tools.push(faker.name.firstName() + " " + i);
    }
    return tools.filter(onlyUnique);
}

export function mockHighLevelAcessData(teamCount, serviceCount, toolCount){

    let mockTeamArray = mockTeamList(teamCount);
    let mockServiceArray = mockServiceList(serviceCount);
    let mockToolArray = mockToolList(toolCount);
    console.log(mockTeamList(teamCount));
    let mockBoardData = [];

    for(let service of mockServiceArray){
        let mockRowData = {
            "service_group": service,
            "teams": {}
        }
        for(let team of mockTeamArray){
            let toolRandomCount = _.random(1, toolCount);
            mockRowData.teams[team] = {
                        "name": faker.company.companySuffix(),
                        "primary_ip": faker.internet.ip(),
                        "os": faker.commerce.product(),
                        "service_group": service,
                        "team_name": team,
                        "tags": [
                          "string 1",
                          "string 2"
                        ],
                        "tools": mockToolArray.slice(0, toolRandomCount).map( (value) =>  {
                          let firstSeen = faker.datatype.number(1640000000, 1649012027);
                          let lastSeen  = faker.datatype.number(firstSeen, 1649012027);
                           return {
                             "tool_name": value, 
                             "last_seen": lastSeen,
                             "first_seen": firstSeen,
                             "total_beacons": faker.datatype.number(4, 30) 
                          }
                      
                        })
                      };
        }
        mockBoardData.push(mockRowData);
    }
    return {"teamList": mockTeamArray, 'serviceList': mockServiceArray, 'toolList': mockToolArray, 'data': mockBoardData };
}

