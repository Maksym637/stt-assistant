import { Navigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { LOGIN_ROUTE } from "../constants/routes";

import { LoadingSpinner } from "../components/element/LoadingSpinner";

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
