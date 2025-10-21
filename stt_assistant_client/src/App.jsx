import { useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { USER_ENDPOINT } from "./constants/apiEndpoints";
import { HOME_ROUTE } from "./constants/routes";

import { useAuthHelper } from "./utils/authHelper";
import { createAxiosInstance } from "./utils/axiosHelper";

import { LoadingSpinner } from "./components/element/LoadingSpinner";
import { UserLoginButton } from "./components/user/UserLoginButton";

import { ProtectedRoute } from "./pages/ProtectedRoute";
import { HomePage } from "./pages/HomePage";

import "./components/user/UserLoginButton.css";

function App() {
  const { isAuthenticated, isLoading, user } = useAuth0();
  const { getAccessToken } = useAuthHelper();

  const navigate = useNavigate();

  useEffect(() => {
    const syncUserWithBackend = async () => {
      const accessToken = await getAccessToken();
      const api = createAxiosInstance(accessToken);

      // --- Process of creating a user ---
      try {
        await api.post(`${USER_ENDPOINT}/create`);
      } catch (error) {
        if (error.response.status === 409) {
          console.error(error.response?.data?.detail);
        } else {
          console.error(`The following error occurred: ${error}`);
        }
      }

      // --- Process of getting a user ---
      try {
        await api.get(`${USER_ENDPOINT}/me`);
      } catch (error) {
        console.error(`The following error occured: ${error}`);
      }

      navigate(HOME_ROUTE);
    };

    if (isAuthenticated && user) {
      syncUserWithBackend();
    }
  }, [isAuthenticated, user]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return (
      <>
        <div className="login-container">
          <p>Please log in to the application first</p>
          <UserLoginButton />
        </div>
      </>
    );
  }

  return (
    <>
      <Routes>
        <Route
          path={HOME_ROUTE}
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

export default App;
