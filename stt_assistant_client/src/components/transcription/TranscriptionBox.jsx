import "./TranscriptionBox.css";

export const TranscriptionBox = ({ text }) => {
  return (
    <>
      <div className="transcription-box">
        <textarea value={text} readOnly rows={10}></textarea>
      </div>
    </>
  );
};
