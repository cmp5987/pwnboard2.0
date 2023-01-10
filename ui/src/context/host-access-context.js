/* eslint-disable react-hooks/exhaustive-deps */
import React, { useCallback, useState } from "react";

export const HostAccessContext = React.createContext({});

export const HostAccessProvider = ({ children }) => {
    const [host, setHost] = useState(null);
    const handleSelectHost = useCallback((newHost) => setHost(newHost), []);
    return (
        <HostAccessContext.Provider
            value={{
                host: host,
                handleSelectHost
            }}>
            {children}
        </HostAccessContext.Provider>
    )
}