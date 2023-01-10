
import { XIcon } from '@heroicons/react/solid';
import React, { useContext, useEffect } from 'react';
import { HostAccessContext } from '../context/host-access-context';

export default function HostAccessSidebar({ showSidebar, setShowSidebar }) {
  const { host: selectedHost, handleSelectHost } = useContext(HostAccessContext);

  useEffect(() => {
    if (selectedHost) {
      setShowSidebar(true);
    }
  }
    , [selectedHost, setShowSidebar]
  )

  if (!selectedHost && !showSidebar) {
    return null;
  }

  const handleCloseButton = () => {
    handleSelectHost(null);
    setShowSidebar(false);
  }

  return (
    <div className='absolute right-0 top-0 h-full w-1/2 md:w-1/4 bg-neutral-800'>
      <button type="button" className="m-2 text-neutral-200 w-full flex flex-row items-center gap-2 justify-center rounded-md border border-neutral-700 shadow-sm px-4 py-2 font-medium hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-white bg-neutral-800 sm:w-auto" onClick={handleCloseButton}>
            <XIcon className="w-4 h-4" />
            <span>Close</span>
      </button>
      <div className='m-2'>
        {selectedHost ?
          <div>Details about Host</div> :
          <div>Filters go Here</div>
        }
      </div>

    </div>
  );
}