import { useAuth0 } from "@auth0/auth0-react";

/**
 * Custom React hook providing helper methods for working with Auth0 authentication
 *
 * @function useAuthHelper
 * @returns {Object} An object containing authentication utility functions
 * @returns {Function} return.getAccessToken - Retrieves a valid Auth0 access token silently
 */
export const useAuthHelper = () => {
  const { getAccessTokenSilently } = useAuth0();

  const getAccessToken = async () => {
    try {
      const accessToken = await getAccessTokenSilently();
      return accessToken;
    } catch (error) {
      console.error(`Error getting token: ${error}`);
      return null;
    }
  };

  return { getAccessToken };
};
