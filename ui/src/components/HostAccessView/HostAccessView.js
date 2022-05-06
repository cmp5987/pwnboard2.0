
import React, { useState } from 'react';
import HostAccessNav from '../HostAccessNav';
import HostAccessSidebar from '../HostAccessSidebar';
import TableQuery from '../TableQuery';

export default function HostAccessView({tableData}) {
  const [showSidebar, setShowSidebar] = useState(false);

  const handleFilterToggleOn = () => {
    setShowSidebar(true);
  }

  return (
    <div className="m-0 w-screen h-screen bg-black text-neutral-400 flex flex-col" >
      <HostAccessNav handleFilterToggleOn={handleFilterToggleOn} />
      <HostAccessSidebar showSidebar={showSidebar} setShowSidebar={setShowSidebar} />
      <div className={`flex-1 overflow-x-scroll overflow-y-scroll scrollbar ${showSidebar && "w-1/2 md:w-3/4"}`}>
        <TableQuery data={tableData}/>
      </div>
    </div>
  );
}