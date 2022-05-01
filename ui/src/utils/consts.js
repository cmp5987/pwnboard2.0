export const serviceList = [
    'Ubuntu DNS',
    'mail',
    'PAN',
    'ad',
    'kali',
    'parrot',
    'volp',
    'web',
    'db',
    'win8',
    'IOT',
    'ADDS Windows',
    'WebServer',
    'Database',
    'Ubuntu Desktop',
    'Rogue Linux',
    'Windows 1'
];

// Potential data returned
// # /curboard # how get to ptr at webserver.
// [
//     {
//         "team_key": "hulto_name"
//         "webserver": {  # No special characters
//             "unsanitized_name": "web server"
//             "ip": "10.0.0.1",
//             "total_access": 5,
//             "current_access": 3,
//         }
//     },
// ]
// # /hostdetails?ips=[IP],[IP]
// [
//     {
//         "team_name": "Hulto"
//         "sg_name": "Hulto"
//         "tools": [
//             {
//                 "tool_name": "reptile",
//                 "last_seen": ''
//             }
//         ]
//     },
// ]
// # /getteams?team_name="Hulto"
// [
//     {
//         "team_name": "Hulto"
//         "team_key": "hulto"
//         "team_id":"team_<Some uuid>"
//     },
// ]
// # /getservicegroups
// [
//     {
//         "sg_key":"webserver"
//         "sg_name": "Web Server"
//         "sg_id":"service_<Some uuid>"
//     },
// ]
// # /gettooldes
// [
//     {
//         "tool_name"
//         "tool_id":"tooldesc_<Some uuid>"
//     }
// ]