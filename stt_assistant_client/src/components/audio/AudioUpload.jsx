import { useState, useRef, useImperativeHandle, forwardRef } from "react";

import "./AudioUpload.css";

export const AudioUpload = forwardRef(({ onFileSelect }, ref) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const fileInputRef = useRef(null);

  useImperativeHandle(ref, () => ({
    reset: () => {
      setAudioUrl(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    },
    setPreview: (file) => {
      const url = URL.createObjectURL(file);
      setAudioUrl(url);
    },
  }));

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
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
});
