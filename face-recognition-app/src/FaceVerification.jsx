import  { useState } from "react";
import axios from "axios";

const FaceVerification = () => {
  const [webcamImage, setWebcamImage] = useState(null);
  const [nidPdf, setNidPdf] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e, type) => {
    if (type === "webcam") setWebcamImage(e.target.files[0]);
    else setNidPdf(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!webcamImage || !nidPdf) {
      setError("Please upload both files.");
      return;
    }

    const formData = new FormData();
    formData.append("webcam_image", webcamImage);
    formData.append("nid_pdf", nidPdf);

    try {
      const response = await axios.post("http://127.0.0.1:5000/verify", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong.");
    }
  };

  return (
    <div>
      <h2>Face Verification</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={(e) => handleFileChange(e, "webcam")} />
        <input type="file" accept=".pdf" onChange={(e) => handleFileChange(e, "nid")} />
        <button type="submit">Verify</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {result && <p>Face Match: {result.matched ? "✅ Matched" : "❌ Not Matched"}</p>}
    </div>
  );
};

export default FaceVerification;
