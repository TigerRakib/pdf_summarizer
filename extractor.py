import fitz
import json
PDF_PATH="Form ADT-1-29092023_signed.pdf"

def extract_text_from_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])



if __name__=="__main__":
    full_text=extract_text_from_pdf(PDF_PATH)
    print(full_text)