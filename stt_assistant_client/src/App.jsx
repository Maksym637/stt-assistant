import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { LoginButton } from "./components/user/UserLoginButton";
import { fetchAccessToken } from "./hooks/authHelper";

function App() {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    if (isAuthenticated) {
      fetchAccessToken(getAccessTokenSilently);
    }
  }, [isAuthenticated, getAccessTokenSilently]);

  if (!isAuthenticated) {
    return (
      <>
        <div>Hello STT-Assistant APP!</div>
        <LoginButton />
      </>
    );
  }
}

export default App;
