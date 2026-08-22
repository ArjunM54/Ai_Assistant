import fitz
import easyocr

reader = easyocr.Reader(['en'])

def read_scanned_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:

        pix = page.get_pixmap()

        image_path = "temp.png"

        pix.save(image_path)

        result = reader.readtext(image_path)

        for item in result:
            text += item[1] + "\n"

    return text