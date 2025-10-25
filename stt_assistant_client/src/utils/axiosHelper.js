import axios from "axios";

import { BASE_API_URL } from "../constants/apiEndpoints";

/**
 * Creates and returns a preconfigured Axios instance with authentication headers
 *
 * This function initializes an Axios client for making HTTP requests to the application's
 * backend API. It automatically includes a Bearer token in the `Authorization` header
 * for authenticated requests
 *
 * @function createAxiosInstance
 * @param {string} accessToken - The Auth0 access token used for authorization
 * @returns {import("axios").AxiosInstance} A configured Axios instance with a base URL and authorization header
 */
export const createAxiosInstance = (accessToken) => {
  return axios.create({
    baseURL: BASE_API_URL,
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
};
