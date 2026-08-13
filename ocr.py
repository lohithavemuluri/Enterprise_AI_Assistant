import pymupdf
import pytesseract
from PIL import Image
import io

# TESSERACT CONFIGURATION

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# OCR PDF FUNCTION

def extract_text_with_ocr(pdf_bytes):

    text = ""

    pdf = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    for page in pdf:

        # Try normal text extraction first
        page_text = page.get_text()

        if page_text.strip():

            text += page_text
            text += "\n"

        else:

            # Convert scanned page to image
            pix = page.get_pixmap(
                dpi=200
            )

            image_bytes = pix.tobytes(
                "png"
            )

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            # Run OCR
            ocr_text = pytesseract.image_to_string(
                image
            )

            text += ocr_text
            text += "\n"

    pdf.close()

    return text