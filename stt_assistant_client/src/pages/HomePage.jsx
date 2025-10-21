import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import {
  RECORD_ENDPOINT,
  TRANSCRIPTION_ENDPOINT,
} from "../constants/apiEndpoints";
import { HISTORY_ROUTE } from "../constants/routes";

import { useAuthHelper } from "../utils/authHelper";
import { createAxiosInstance } from "../utils/axiosHelper";

import { LoadingSpinner } from "../components/element/LoadingSpinner";
import { AudioUpload } from "../components/audio/AudioUpload";
import { TranscriptionBox } from "../components/transcription/TranscriptionBox";
import { UserLogoutButton } from "../components/user/UserLogoutButton";

import "./HomePage.css";

export const HomePage = () => {
  const { user, isAuthenticated } = useAuth0();
  const { getAccessToken } = useAuthHelper();

  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [transcription, setTranscription] = useState("");

  const [loading, setLoading] = useState(false);

  const handleUpload = (f) => {
    setFile(f);
    setTranscription("");
  };

  const handleProcess = async () => {
    if (!file) {
      return alert("Please upload an audio file first.");
    }

    setLoading(true);

    try {
      const accessToken = await getAccessToken();
      const api = createAxiosInstance(accessToken);

      const formData = new FormData();
      formData.append("file", file);

      const recordResponse = await api.post(
        `${RECORD_ENDPOINT}/create`,
        formData
      );

      const transcriptionResponse = await api.post(
        `${TRANSCRIPTION_ENDPOINT}/create`,
        {
          record_id: recordResponse.data.id,
          language_code: "en-US",
        }
      );

      setTranscription(transcriptionResponse.data.transcription);
    } catch (error) {
      alert(error.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <LoadingSpinner />;
  }

  return (
    <>
      <header className="home-header">
        <button onClick={() => navigate(HISTORY_ROUTE)} className="history-btn">
          History
        </button>
        <UserLogoutButton email={user?.email} />
      </header>

      <main className="home-content">
        <h2>Upload and Process Audio</h2>
        <AudioUpload onFileSelect={handleUpload} />

        <button
          onClick={handleProcess}
          disabled={loading}
          className="process-button"
        >
          {loading ? "Processing..." : "Perform audio processing"}
        </button>

        {transcription && <TranscriptionBox text={transcription} />}
      </main>
    </>
  );
};
