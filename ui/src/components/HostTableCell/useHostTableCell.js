import { useState } from "react";

export function useHostTableCell(cellData) {
    //logic for Host Access Goes Here
    const [activeToolCount, ] = useState(
        getCountOfActiveTools(cellData.tools, 5)
    );

    let accessColor = getAccessCellColor(activeToolCount, cellData.tools.length);

    function getAccessCellColor(activeCount, totalCount) {
        let alarmingAccessCount = 3;

        if (activeCount === totalCount) {
            return "bg-green-900/50";
        }
        else if (activeCount === 0) {
            return "bg-red-900/25";
        }
        else if (activeCount < alarmingAccessCount) {
            return "bg-red-700";
        }
        else {
            return "bg-red-700/50"
        }
    }

    function getCountOfActiveTools(tools, minutesTillInactive) {
        // Get current date as EPOC
        let currentTime = Math.floor(new Date().getTime() / 1000.0);

        // Time when tool is considered inactive
        let inactiveTime = currentTime - (minutesTillInactive * 60);

        // Sum tools to get active tools by last seen EPOC
        let activeCount = tools.reduce(function (accumulator, tool) {
            if (tool.last_seen >= inactiveTime) {
                return accumulator + 1;
            }
            return accumulator;
        }, 0);

        return activeCount;
    }

    return {
        activeToolCount,
        accessColor
    }
}