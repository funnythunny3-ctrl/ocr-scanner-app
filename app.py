import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import io

st.set_page_config(page_title="OCR Scanner App", layout="centered")
st.title("📄 OCR Scanner: Images & PDFs")

st.write("""
Upload an **image** (png/jpg/jpeg) or a **PDF** file, and extract the text.
""")

# File uploader
uploaded_file = st.file_uploader("Choose an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

if uploaded_file:
    file_type = uploaded_file.type
    if file_type in ["image/png", "image/jpeg", "image/jpg"]:
        # Handle image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Extract Text from Image"):
            text = extract_text_from_image(image)
            st.subheader("Extracted Text:")
            st.text_area("", text, height=200)
            # Download button
            st.download_button("Download Text", text, file_name="extracted_text.txt")
    elif file_type == "application/pdf":
        # Handle PDF
        pages = convert_from_bytes(uploaded_file.read())
        all_text = ""
        for i, page in enumerate(pages):
            st.image(page, caption=f"Page {i+1}", use_column_width=True)
            all_text += extract_text_from_image(page) + "\n\n"
        if st.button("Extract Text from PDF"):
            st.subheader("Extracted Text:")
            st.text_area("", all_text, height=200)
            st.download_button("Download Text", all_text, file_name="extracted_text.txt")
    else:
        st.warning("Unsupported file type!")
