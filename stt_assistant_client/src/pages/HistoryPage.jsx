import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { TRANSCRIPTION_ENDPOINT } from "../constants/apiEndpoints";
import { HOME_ROUTE } from "../constants/routes";

import { useAuthHelper } from "../utils/authHelper";
import { createAxiosInstance } from "../utils/axiosHelper";

import { LoadingSpinner } from "../components/element/LoadingSpinner";
import { UserLogoutButton } from "../components/user/UserLogoutButton";

import "./HistoryPage.css";

export const HistoryPage = () => {
  const { user, isAuthenticated } = useAuth0();
  const { getAccessToken } = useAuthHelper();

  const navigate = useNavigate();

  const [transcriptions, setTranscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  // --- Process of getting all transcriptions ---
  useEffect(() => {
    const syncTranscriptionsWithBackend = async () => {
      try {
        const accessToken = await getAccessToken();
        const api = createAxiosInstance(accessToken);

        const transcriptionsResponse = await api.get(
          `${TRANSCRIPTION_ENDPOINT}/all`
        );
        setTranscriptions(transcriptionsResponse.data.data);
      } catch (error) {
        alert(`[${error.response.status}] ${error.response.data.detail}`);
      } finally {
        setLoading(false);
      }
    };

    syncTranscriptionsWithBackend();
  }, [isAuthenticated]);

  if (!isAuthenticated || loading) {
    return <LoadingSpinner />;
  }

  return (
    <>
      <header className="history-header">
        <button onClick={() => navigate(HOME_ROUTE)} className="home-btn">
          Home
        </button>
        <UserLogoutButton email={user?.email} />
      </header>
      <main className="history-content">
        {transcriptions.length === 0 ? (
          <p className="no-transcriptions">
            There are no transcriptions available at this time
          </p>
        ) : (
          <div className="transcription-list">
            {transcriptions.map((item, index) => (
              <div key={index} className="transcription-item">
                <audio
                  controls
                  src={item.audio_url}
                  className="audio-player"
                ></audio>
                <div className="transcription-text">
                  <p>{item.transcription}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
};
