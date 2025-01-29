import { extractImageFromPDF } from "../utils/pdfExtractor";


const NIDUpload = (props) => {
  const { setExtractedImage }=props||{}
  const handleNidPdfChange = async (e) => {
    const pdfFile = e.target.files[0];
    // setNidPdf(pdfFile);
// console.log(pdfFile)
    try {
      const imageUrl = await extractImageFromPDF(pdfFile);
      setExtractedImage(imageUrl);
      console.log("Extracted Image:", imageUrl);
    } catch (error) {
      console.error("Error extracting image from PDF:", error);
      alert("No image found in PDF.");
    }
  };

  return (
    <div>
      <input type="file" accept="application/pdf" onChange={handleNidPdfChange} />
    </div>
  );
};

export default NIDUpload;