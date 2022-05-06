import axios from "axios";
import { useQuery } from "react-query";
import { getBackendBaseUrl } from "../utils/utils";

export function useBoard() {
    //logic for Host Access Goes Here
    return useQuery("getBoard", async () => {
        let url = getBackendBaseUrl() + "/getBoard";
        const out = await axios.get(url);
        return out.data;
      });
}