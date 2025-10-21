import { useAuth0 } from "@auth0/auth0-react";

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
