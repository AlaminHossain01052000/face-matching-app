from flask import Flask, request, jsonify
from flask_cors import CORS
from pikepdf import Pdf, PdfImage
import face_recognition
from PIL import Image
import numpy as np
import os
app = Flask(__name__)
CORS(app)

def are_faces_similar(image_path1, image_path2):
    try:
        # Open and convert the images to RGB (if not already in RGB mode)
        image1 = Image.open(image_path1).convert("RGB")
        image2 = Image.open(image_path2).convert("RGB")

        # Load the images using face_recognition
        image1 = np.array(image1)
        image2 = np.array(image2)

        # Find all faces in the images
        face_locations1 = face_recognition.face_locations(image1)
        face_locations2 = face_recognition.face_locations(image2)

        # Check if no faces are detected in any of the images
        if len(face_locations1) == 0:
            return "No face detected in the first image."
        if len(face_locations2) == 0:
            return "No face detected in the second image."

        # Assuming there's only one face per image, get the first face found
        face_encoding1 = face_recognition.face_encodings(image1, face_locations1)[0]
        face_encoding2 = face_recognition.face_encodings(image2, face_locations2)[0]

        # Compare the faces
        results = face_recognition.compare_faces([face_encoding1], face_encoding2)

        if results[0]:
            return True
        else:
            return False

    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/upload", methods=["POST"])
def upload_files():
    # Check if files are in the request
    if "pdf_file" not in request.files or "image_file" not in request.files:
        return jsonify({"error": "Missing files"}), 400
    
    pdf_file = request.files["pdf_file"]
    image_file = request.files["image_file"]
    
    # =========== Extracting the image from pdf starts here
    pdf_path = "uploaded_pdf.pdf"
    pdf_file.save(pdf_path)
    
    try:
        # Open the PDF
        old_pdf = Pdf.open(pdf_path)
        page_1 = old_pdf.pages[0]
        print(list(page_1.images.keys()))
        # Check if the page contains images
        images = page_1.images
        if not images:
            return jsonify({"error": "No images found in PDF"}), 400
        
        # Check if the specific image key exists (for example, "/Im2")
        image_key = "/Im2"
        if image_key not in images:
            return jsonify({"error": f"Image with key {image_key} not found in PDF"}), 400
        
        raw_image2 = images[image_key]
        pdf_image = PdfImage(raw_image2)
        pdf_image.extract_to(fileprefix="nid-image")
        
        
        # ======== Save the image from the uploaded file starts here
        image_path1 = "uploaded_image.png"
        image_file.save(image_path1)
        # ======== Save the image ends here
    
        image_path2 = "nid-image.jpg"
        result = are_faces_similar(image_path1, image_path2)
        
        print(f"Image extracted successfully from PDF.")
        # Delete image files after processing
        try:
            if os.path.exists(image_path1):
                os.remove(image_path1)
            if os.path.exists(image_path2):
                os.remove(image_path2)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            print(f"Error while deleting files: {str(e)}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

    

    # Optionally, you can return the file details as a JSON response
    return jsonify({
        "pdf_file": {
            "filename": pdf_file.filename,
            "content_type": pdf_file.content_type
        },
        "image_file": {
            "filename": image_file.filename,
            "content_type": image_file.content_type
        },
        "result":result
    })

if __name__ == "__main__":
    app.run(debug=True)
