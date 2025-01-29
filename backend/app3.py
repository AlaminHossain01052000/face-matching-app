from pdf2image import convert_from_path
import face_recognition
from PIL import Image
import numpy as np
import io

# Step 1: Convert PDF pages to images
def extract_images_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        image_data = []
        for img in images:
            # Convert each page image to byte data
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            image_data.append(img_byte_arr.read())
        return image_data
    except Exception as e:
        print(f"Error extracting images from PDF: {e}")
        return []

# Step 2: Detect faces in the image
def detect_faces(image_data):
    image = Image.open(io.BytesIO(image_data))
    img_array = np.array(image)
    
    # Detect faces using face_recognition
    face_locations = face_recognition.face_locations(img_array)
    
    return face_locations, img_array

# Step 3: Crop face and save it
def crop_face(image_data, face_location):
    top, right, bottom, left = face_location
    image = Image.open(io.BytesIO(image_data))
    face_image = image.crop((left, top, right, bottom))
    return face_image

# Main function
def extract_face_from_pdf(pdf_path):
    images = extract_images_from_pdf(pdf_path)
    
    for img_data in images:
        face_locations, img_array = detect_faces(img_data)
        
        if face_locations:
            for face_location in face_locations:
                face_image = crop_face(img_data, face_location)
                face_image.save("extracted_face.png")
                print("Face extracted and saved.")
        else:
            print("No faces detected in the image.")

# Example usage
pdf_path = "uploaded_pdf.pdf"
extract_face_from_pdf(pdf_path)
