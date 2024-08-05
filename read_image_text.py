from PIL import Image
import pytesseract

BASE_PATH = 'images/'

image_path = BASE_PATH + 'enel.jpg'
# image = Image.open(image_path)
# text = pytesseract.image_to_string(image)
# print(text)

# # Converter texto para minúsculo
# if 'eletropaulo' in text.lower():
#     print('Enel is in the text')

# Usando easyocr
import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext(image_path)
print(result)

if 'eletropaulo' in result[0][1].lower():
    print('Enel is in the text')
