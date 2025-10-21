import { Navigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { LOGIN_ROUTE } from "../constants/routes";

import { LoadingSpinner } from "../components/element/LoadingSpinner";

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return isAuthenticated ? children : <Navigate to={LOGIN_ROUTE} />;
};
