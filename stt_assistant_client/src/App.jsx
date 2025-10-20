import { Routes, Route } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { UserLoginButton } from "./components/user/UserLoginButton";

import { ProtectedRoute } from "./pages/ProtectedRoute";
import { HomePage } from "./pages/HomePage";

function App() {
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return (
      <>
        <div>
          <h1>Hello STT-Assistant APP!</h1>
          <p>Please log in to continue</p>
          <UserLoginButton />
        </div>
      </>
    );
  }

  return (
    <>
      <Routes>
        <Route
          path="/"
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
