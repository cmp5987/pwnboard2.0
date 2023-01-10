
import { ArrowNarrowLeftIcon, FilterIcon } from '@heroicons/react/solid';
import React from 'react';

export default function HostAccessNav({handleFilterToggleOn}){
  return (
    <div className="flex flex-row justify-between px-1 py-2 sticky items-center bg-neutral-900">
        <button type="button" className="outline-button" onClick={() => console.log("here")}>
            <ArrowNarrowLeftIcon className="w-4 h-4"/>
            <span>Back</span>
        </button>
        <h1 className="text-lg font-semibold text-neutral-300"> PwnBoard 2.0 - Host Access Table</h1>
        <button type="button" className="outline-button" onClick={handleFilterToggleOn}>
            <FilterIcon className='w-4 h-4'/>
            <span>Adjust Filters</span>
        </button>
    </div>
  );
}