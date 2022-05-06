
import React, { useContext } from 'react';
import { HostAccessContext } from '../../context/host-access-context';
import { useHostTableCell } from './useHostTableCell';

export default function HostTableCell({ cellData }) {
    const { host: selectedHost, handleSelectHost } = useContext(HostAccessContext);
    const { activeToolCount, accessColor } = useHostTableCell(cellData);

    const handleCellClick = () => {
        if (selectedHost?.primary_ip !== cellData.primary_ip) {
            console.log(cellData);
            handleSelectHost(cellData);
        }
    }

    return (
        <div className={`p-1 text-neutral-300 flex flex-col gap-1 rounded shadow-sm items-center hover:cursor-pointer hover:bg-neutral-700 hover:shadow-md ${accessColor}`} onClick={handleCellClick} tabIndex={0}>
            <div className="font-medium">
                {cellData.primary_ip}
            </div>
            <div className={`w-full rounded flex flex-row justify-center`}>
                <span>
                    {activeToolCount} / {cellData.tools.length}
                </span>
            </div>
        </div>
    );
}