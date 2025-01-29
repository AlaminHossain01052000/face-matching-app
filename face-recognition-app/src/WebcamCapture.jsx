import { useRef } from "react";
import Webcam from "react-webcam";

const WebcamCapture = (props) => {
  const { setCapturedImage, setImageFile, capturedImage, imageFile } = props || {}
  const webcamRef = useRef(null);

  const handleCapture = () => {
    if (webcamRef.current) {
      // Capture image using the webcam
      const imageData = webcamRef.current.getScreenshot();
      // Convert the captured base64 image to a JPG file
      const byteArray = new Uint8Array(atob(imageData.split(",")[1]).split("").map((c) => c.charCodeAt(0)));
      const file = new File([byteArray], "captured-image.jpg", { type: "image/jpeg" });
      setCapturedImage(file);
      setImageFile(imageData)
      // handleSubmit()
    }
  };
  return (
    <div>
      <div>
        <label>Capture Image:</label>
        <Webcam
          audio={false}
          screenshotFormat="image/jpeg"
          width="100%"
          ref={webcamRef} // Pass the reference here
        />
        {capturedImage && (
          <div>

            <h6>Captured Image</h6>
            <img
              src={imageFile}
              alt="Captured"
              style={{ width: "100%", height: "auto", objectFit: "cover" }}
            />

          </div>
        )}
      </div>
      <button type="button" onClick={handleCapture}>
        Capture Image
      </button>
    </div>

  );
};

export default WebcamCapture;