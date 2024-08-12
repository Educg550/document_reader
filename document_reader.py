import os
import easyocr

from glob import glob
from tqdm import tqdm

import matplotlib.pyplot as plt

"""### Imagens puras"""

# JPG, cada sublista de img_fns é uma lista com todas as imagens de um mesmo documento
img_fns = []

def show_image(image_path):
  fig, ax = plt.subplots(figsize=(10, 10))
  ax.imshow(plt.imread(image_path))
  plt.axis('off')
  plt.show()

for img_list in img_fns:
  for img in img_list:
    show_image(img)

"""#### EasyOCR"""

def which_company(text):
  company_matches = {
    'enel': {'enei', 'enel', 'eletropaulo', 'eietropaulo', 'eletropauio', 'eietropauio', 'eletropau', 'eietropau'},
    'cemig': {'cemig', 'cemlg', 'cenig', 'cenlg'}
  }
  words = set(word.lower() for word in text.split())
  for company, matches in company_matches.items():
    if words & matches:
      return company

ocr_reader = easyocr.Reader(['en'], gpu = True)

results = []

for img_list in tqdm(img_fns):
  sub_results = []
  for img in img_list:
    sub_results.append(ocr_reader.readtext(img))
  results.append(sub_results)

len(results)

text_extracted = []

for document in results:
  text_document = []
  for page in document:
    for tupl in page:
      text_document.append(tupl[1])
  text_extracted.append(text_document)

len(text_extracted)

# Encontrou a palavra 'enei'
print(text_extracted[0])

for idx, text_document in enumerate(text_extracted, start=0):
  print(f'Documento {img_fns[idx][0]}')
  print(which_company(' '.join(text_document)))

"""#### Extraindo texto puro"""

# Salvando textos extraídos para BASE_PATH/texts
for idx, text_document in enumerate(text_extracted, start=0):
    if img_fns[idx] and isinstance(img_fns[idx][0], str):
        filename = os.path.basename(img_fns[idx][0])[:-4] + '.txt'
        filepath = os.path.join(BASE_PATH, 'texts', filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(' '.join(text_document))
    else:
        print(f"Warning: img_fns[{idx}][0] is not a valid string.")
