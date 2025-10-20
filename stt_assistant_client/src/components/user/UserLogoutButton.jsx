import { useState } from "react";

// import { useAuth0 } from "@auth0/auth0-react";

import "./UserLogoutButton.css";

export const UserLogoutButton = ({ email }) => {
  // const { logout } = useAuth0();
  const [open, setOpen] = useState(false);

  const initial = email ? email.charAt(0).toUpperCase() : "?";

  return (
    <>
      <div className="user-menu">
        <div className="user-icon" onClick={() => setOpen(!open)}>
          {initial}
        </div>
        {/* {open && (
          <div className="user-dropdown">
            <button
              onClick={() =>
                logout({ logoutParams: { returnTo: window.location.origin } })
              }
            >
              Log out
            </button>
          </div>
        )} */}
      </div>
    </>
  );
};
