
import streamlit as st
import pytesseract
from docx import Document
from PIL import Image
import io
import tempfile

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Title of the app
st.title("Image to Word Converter")

# Instructions
# st.write("Upload any image file (JPEG, PNG, or others). The app will convert it to PNG format, extract text, and provide the option to download it as a Word document.")

# Upload the image (supports drag and drop)
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "bmp", "tiff"], label_visibility="collapsed")

if uploaded_file is not None:
    # Open the uploaded image using PIL
    image = Image.open(uploaded_file)

    # Convert image to PNG format (if not already in PNG, JPG, or JPEG)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file, format="PNG")
        temp_file_path = temp_file.name

    # Open the saved PNG image for text extraction
    image = Image.open(temp_file_path)

    # Extract text from the image using pytesseract
    text = pytesseract.image_to_string(image)

    # Create a Word document from the extracted text
    doc = Document()
    doc.add_paragraph(text)

    # Save the document to a byte stream
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    # Provide a download button for the Word file
    st.download_button(
        label="Download as Word Document",
        data=output_stream,
        file_name="extracted_text.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
