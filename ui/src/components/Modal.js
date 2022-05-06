
import React from 'react';

export default function Modal({handleClose = null}){
  return (
    <div className="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-neutral-900 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="relative inline-block align-bottom bg-neutral-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
            <div className="bg-neutral-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                    <h3 className="text-lg leading-6 font-medium text-neutral-200" id="modal-title">Host Details</h3>
                    <div className="mt-2">
                    <p className="text-sm">Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.</p>
                    </div>
                    <div className="mt-2">
                    <p className="text-sm">Are you sure you want to deactivate your account? All of your data will be permanently removed. This action cannot be undone.</p>
                    </div>
                </div>
                </div>
            </div>
            <div className="bg-neutral-800 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                {/* <button type="button" className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm">Deactivate</button> */}
                <button type="button" className="mt-3 text-neutral-200 w-full inline-flex justify-center rounded-md border border-neutral-600 shadow-sm px-4 py-2 text-base font-medium hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-white bg-neutral-800 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm" onClick={handleClose}>Close Details</button>
            </div>
            </div>
        </div>
    </div>
  );
}