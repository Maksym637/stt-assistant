import { useState, useRef } from "react";

import "./AudioUpload.css";

export const AudioUpload = ({ onFileSelect }) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setAudioUrl(url);
      onFileSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <>
      <div
        className="audio-upload"
        onClick={!audioUrl ? handleClick : undefined}
      >
        <input
          type="file"
          accept="audio/*"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: "none" }}
        />

        {!audioUrl && (
          <span className="upload-placeholder">
            Click here to upload audio 📁
          </span>
        )}
        {audioUrl && <audio controls src={audioUrl}></audio>}
      </div>
    </>
  );
};
