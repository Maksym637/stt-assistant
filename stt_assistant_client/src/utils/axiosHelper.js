import axios from "axios";

import { BASE_API_URL } from "../constants/apiEndpoints";

export const createAxiosInstance = (accessToken) => {
  return axios.create({
    baseURL: BASE_API_URL,
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
};
