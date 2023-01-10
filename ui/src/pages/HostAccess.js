import React from "react";
import HostAccessView from "../components/HostAccessView";
import { HostAccessProvider } from "../context/host-access-context";
import { mockHighLevelAcessData } from "../fixtures/utils";



function HostAccess() {
  let testData = mockHighLevelAcessData(20, 20, 10);
  console.log(testData);
  return (
    <HostAccessProvider>
      <HostAccessView tableData={testData}/>
    </HostAccessProvider>
  );
}
export default HostAccess;
