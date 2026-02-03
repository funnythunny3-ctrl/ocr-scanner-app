import streamlit as st
from PIL import Image
import easyocr
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="OCR Scanner App", layout="centered")
st.title("📄 OCR Scanner: Images & PDFs (EasyOCR)")

st.write("""
Upload an **image** (png/jpg/jpeg) or a **PDF** file, and extract text.
""")

uploaded_file = st.file_uploader("Choose an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

reader = easyocr.Reader(['en'])

def extract_text_easyocr(image):
    results = reader.readtext(image, detail=0)
    return "\n".join(results)

if uploaded_file:
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Extract Text from Image"):
            text = extract_text_easyocr(image)
            st.subheader("Extracted Text:")
            st.text_area("", text, height=200)
            st.download_button("Download Text", text, file_name="extracted_text.txt")
    elif uploaded_file.type == "application/pdf":
        pdf_data = uploaded_file.read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        all_text = ""
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(image, caption=f"Page {page_number}", use_column_width=True)
            all_text += extract_text_easyocr(image) + "\n\n"
        if st.button("Extract Text from PDF"):
            st.subheader("Extracted Text:")
            st.text_area("", all_text, height=200)
            st.download_button("Download Text", all_text, file_name="extracted_text.txt")
    else:
        st.warning("Unsupported file type!")

