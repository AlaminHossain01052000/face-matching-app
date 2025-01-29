import  { useState } from "react";

import WebcamCapture from "./WebcamCapture";

function FileUpload() {
  const [pdfFile, setPdfFile] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);

  // Reference to the Webcam component

  const handlePdfChange = (e) => {
    setPdfFile(e.target.files[0]);
  };



  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure both files are selected
    if (!pdfFile || !capturedImage) {
      alert("Please select both a PDF and capture an image.");
      return;
    }

    // Create FormData object to send files
    const formData = new FormData();
    formData.append("pdf_file", pdfFile);
    formData.append("image_file", capturedImage);

    try {
      // Send POST request to Flask server
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      // Handle response
      const result = await response.json();
      if (response.ok) {
        alert("Files uploaded successfully");
        setImageFile(null)
        setCapturedImage(null)
        console.log(result);
      } else {
        alert("Error uploading files");
        console.log(result);
      }
    } catch (error) {
      alert("An error occurred while uploading files.");
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Upload PDF and Capture Image</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>PDF File:</label>
          <input type="file" accept=".pdf" onChange={handlePdfChange} />
        </div>
    <WebcamCapture 
      imageFile={imageFile} 
      capturedImage={capturedImage} 
      setCapturedImage={setCapturedImage} 
      setImageFile={setImageFile}
    />
       

        <button type="submit">Upload</button> 
      </form>
    </div>
  );
}

export default FileUpload;
