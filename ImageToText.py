#                  IMPORTANT!!
# Go to: https://github.com/UB-Mannheim/tesseract/wiki
# Install the executable and come back to the script

from PIL import Image
from pytesseract import pytesseract 
import enum

class OS(enum.Enum):
    Mac = 0
    Windows = 1

class Language(enum.Enum):
    ENG = 'eng'
    RUS = 'rus'
    ITA = 'ita'

class ImageReader:
    def __init__(self, os: OS):
        if os == OS.Mac:
            print('Running on: Mac\n')
        if os == OS.Windows:
            # Replace the address for the one you saved it when you installed it
            # I installed it on that address. Change it.
            # For that, your need to install the PyTesseract first
            Windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd = Windows_path
            print('Running on: Windows\n')

    def extract_text(self, image: str, lang: str) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang)
        return extracted_text

if __name__ == '__main__':
    ir = ImageReader(OS.Windows)
    # This is the address where you have your image to be converted.
    text = ir.extract_text('D:\py\ss1.png', Language.ENG.value)
    print(text)
