// import  { useState } from "react";
// import WebcamCapture from "./WebcamCapture";
// import NIDUpload from "./NIDUpload";
// import axios from "axios";
// import FaceVerification from "./FaceVerification";
import FileUpload from "./FileUpload";

const App = () => {
  // const [webcamImage, setWebcamImage] = useState(null);
  // const [extractedImage, setExtractedImage] = useState(null);
  // const [verificationResult, setVerificationResult] = useState(null);

  // const handleVerify = async () => {
  //   if (webcamImage && extractedImage) {
  //     const formData = new FormData();
  //     formData.append("webcam_image", webcamImage);
  //     formData.append("nid_pdf", extractedImage);
  //     for(let ele of formData.entries()){
  //       console.log(ele)
  //     }
  //     try {
  //       const response = await axios.post("http://127.0.0.1:5000/verify", formData, {
  //         headers: {
  //           "Content-Type": "multipart/form-data"
  //         }
  //       })
  //       setVerificationResult(response.data.matched ? "Matched" : "Not Matched");
  //     } catch (error) {
  //       console.error("Error verifying:", error);
  //     }
  //   }
  // };

  return (
    <div>
      <FileUpload/>
      {/* <FaceVerification/> */}
      {/* <WebcamCapture setWebcamImage={setWebcamImage} />
      <NIDUpload setExtractedImage={setExtractedImage} />
      <button onClick={handleVerify}>Verify</button>
      {verificationResult && <p>{verificationResult}</p>} */}
    </div>
  );
};

export default App;