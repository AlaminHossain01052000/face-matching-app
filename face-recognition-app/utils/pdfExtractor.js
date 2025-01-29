import * as pdfjsLib from "pdfjs-dist";
import "pdfjs-dist/build/pdf.worker";

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

export async function extractImageFromPDF(pdfFile) {
  const reader = new FileReader();

  return new Promise((resolve, reject) => {
    reader.onload = async function () {
      try {
        const pdfData = new Uint8Array(reader.result);
        const pdf = await pdfjsLib.getDocument({ data: pdfData }).promise;
        const page = await pdf.getPage(1); // Single-page PDF

        // Set a high scale factor for better resolution
        const scale = 2;
        const viewport = page.getViewport({ scale });

        const canvas = document.createElement("canvas");
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        const ctx = canvas.getContext("2d");

        const renderTask = page.render({
          canvasContext: ctx,
          viewport: viewport,
        });

        await renderTask.promise;

        // ⚡ Manually Crop the Image Region (Modify X, Y, Width, Height)
        const cropX = canvas.width * 0.7; // 70% from the left
        const cropY = canvas.height * 0.1; // 10% from the top
        const cropWidth = canvas.width * 0.25; // 25% of page width
        const cropHeight = canvas.height * 0.35; // 35% of page height

        const croppedCanvas = document.createElement("canvas");
        croppedCanvas.width = cropWidth;
        croppedCanvas.height = cropHeight;
        const croppedCtx = croppedCanvas.getContext("2d");

        croppedCtx.drawImage(
          canvas,
          cropX, // Start X
          cropY, // Start Y
          cropWidth, // Crop Width
          cropHeight, // Crop Height
          0,
          0,
          cropWidth,
          cropHeight
        );

        // Convert Cropped Image to Base64
        const imageUrl = croppedCanvas.toDataURL("image/jpeg");

        resolve(imageUrl);
      } catch (error) {
        reject(error);
      }
    };

    reader.readAsArrayBuffer(pdfFile);
  });
}
