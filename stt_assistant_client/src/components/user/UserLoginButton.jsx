import { useAuth0 } from "@auth0/auth0-react";

import "./UserLoginButton.css";

export const UserLoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <>
      <button onClick={() => loginWithRedirect()}>Log In</button>
    </>
  );
};
