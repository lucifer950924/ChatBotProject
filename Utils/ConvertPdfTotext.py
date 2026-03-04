from pdf2image import convert_from_path
import pytesseract

def convertImagetoText(path):
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    images = convert_from_path(path)
    full_text = ''
    for image in images:
        text = pytesseract.image_to_string(image,lang='ben')
        full_text += text +'\n'

    return full_text



