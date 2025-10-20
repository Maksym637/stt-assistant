import axios from "axios";

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth0 } from "@auth0/auth0-react";

import { useAuthHelper } from "../hooks/authHelper";

import { AudioUpload } from "../components/audio/AudioUpload";
import { TranscriptionBox } from "../components/transcription/TranscriptionBox";
import { UserLogoutButton } from "../components/user/UserLogoutButton";

import "./HomePage.css";

const baseUrl = "TODO"; // TBD

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
    if (!file) return alert("Please upload an audio file first.");
    setLoading(true);

    try {
      const token = await getAccessToken();

      const formData = new FormData();
      formData.append("file", file);

      const recordRes = await axios.post(`${baseUrl}/record/create`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      const recordId = recordRes.data.id;

      const transRes = await axios.post(
        `${baseUrl}/transcription/create`,
        {
          record_id: recordId,
          language_code: "en-US",
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setTranscription(transRes.data.transcription);
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Error during audio processing.");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <p>Loading...</p>;
  }

  return (
    <>
      <div className="home-container">
        <header className="home-header">
          <button onClick={() => navigate("/history")} className="history-btn">
            History
          </button>
          <UserLogoutButton email={user?.email} />
        </header>

        <main className="home-content">
          <h2>Upload and Process Audio</h2>
          <AudioUpload onFileSelect={handleUpload} />

          <button onClick={handleProcess} disabled={loading}>
            {loading ? "Processing..." : "Perform audio processing"}
          </button>

          {transcription && <TranscriptionBox text={transcription} />}
        </main>
      </div>
    </>
  );
};
