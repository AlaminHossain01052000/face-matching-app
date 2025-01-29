import face_recognition
import numpy as np
import fitz  # PyMuPDF for extracting images from PDF
import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
from PIL import Image
import numpy as np

def convert_image_to_rgb(image_path):
    # Open the image with PIL and convert to RGB
    image = Image.open(image_path)
    rgb_image = image.convert("RGB")
    # Save the converted image temporarily
    rgb_image_path = os.path.join(tempfile.gettempdir(), "converted_image.jpg")
    rgb_image.save(rgb_image_path)
    return rgb_image_path

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_images_from_pdf(pdf_path):
    """Extract the first image from a PDF."""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        if image_list:
            xref = image_list[0][0]  # Get first image
            base_image = pdf_document.extract_image(xref)
            return base_image["image"]
    return None  # No image found

def encode_face(image_path):
    """Get face encoding from an image file."""
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

@app.route("/verify", methods=["POST"])
def verify():
    if "webcam_image" not in request.files or "nid_pdf" not in request.files:
        return jsonify({"error": "Missing files"}), 400

    webcam_image = request.files["webcam_image"]
    nid_pdf = request.files["nid_pdf"]

    if not (allowed_file(webcam_image.filename) and allowed_file(nid_pdf.filename)):
        return jsonify({"error": "Invalid file type"}), 400

    # Save webcam image
    webcam_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(webcam_image.filename))
    webcam_image.save(webcam_path)

    # Save and extract image from NID PDF
    nid_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(nid_pdf.filename))
    nid_pdf.save(nid_path)

    nid_image_data = extract_images_from_pdf(nid_path)
    if not nid_image_data:
        return jsonify({"error": "No images found in PDF"}), 400

    nid_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "nid_extracted.jpg")
    with open(nid_image_path, "wb") as f:
        f.write(nid_image_data)

    # Get face encodings
    webcam_encoding = encode_face(webcam_path)
    nid_encoding = encode_face(nid_image_path)

    if webcam_encoding is None or nid_encoding is None:
        return jsonify({"error": "No face detected in one or both images"}), 400

    # Compare faces
    matched = face_recognition.compare_faces([webcam_encoding], nid_encoding)[0]

    return jsonify({"matched": matched})

if __name__ == "__main__":
    app.run(debug=True)
