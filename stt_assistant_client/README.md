### FE part

---

### Coding points

1. Implementation of the `useAuthHelper` function:

```js
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
```

2. Implementation of the `createAxiosInstance` function:

```js
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
```

3. Implementation of the `ProtectedRoute` component:

```js
/**
 * A higher-order component that protects routes by requiring authentication
 *
 * This component checks the user's authentication state using Auth0. While
 * the authentication status is loading, it displays a loading spinner.
 * If the user is authenticated, it renders the child components.
 * Otherwise, it redirects the user to the login page
 *
 * @component
 * @param {Object} props - React component props
 * @param {React.ReactNode} props.children - The content to render if the user is authenticated
 * @returns {React.ReactNode} The child components if authenticated, a loading spinner if loading,
 *                            or a `<Navigate>` component redirecting to the login route
 */
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return isAuthenticated ? children : <Navigate to={LOGIN_ROUTE} />;
};
```

---

### Improvements to consider

- Create a cleaner separation of components into functional and JSX parts

---
