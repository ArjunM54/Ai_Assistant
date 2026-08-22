from pypdf import PdfReader

def read_pdf(pdf_path):
    #this reader reades from the file.
    reader = PdfReader(pdf_path)

    #print the length of the file.
    """length=len(reader.pages)
    print(length)"""

    #prints the first page of the file.
    """firstpage=reader.pages[0]
    print(firstpage.extract_text())"""

    #used to extract all the text from the file.
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    """for i, page in enumerate(reader.pages):
    
        page_text = page.extract_text()
    
        print(f"Page {i+1}:", page_text)"""

    return text

