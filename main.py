import easyocr

from google_trans_new import google_translator

import cv2


IMAGE_PATH = './assets/test.jpg'

IMAGE_EXTENSION = '.jpg'

LANGUAGE_ORIGIN = 'en'

LANGUAGE_TARGET = 'pt'


# OCR
reader = easyocr.Reader([LANGUAGE_ORIGIN], gpu=True)

result = reader.readtext(IMAGE_PATH, paragraph=False)


# Translation
translator = google_translator()


def translate(text):
    translate_text = translator.translate(
        text,
        lang_src=LANGUAGE_ORIGIN,
        lang_tgt=LANGUAGE_TARGET,
		pronounce=False
    )

    return translate_text


# Image
image = cv2.imread(IMAGE_PATH)

for sentence in reversed(result):
    boxes, text, confident = sentence

    cv2.rectangle(
        image,  # Source image
        tuple(boxes[0]),  # Upper left corner vertex
        (boxes[1][0], boxes[2][1]),  # Lower right corner vertex
        (255, 255, 255),  # Color
        -1,
    )

    translate_text = translate(text)

    cv2.putText(
        image,  # Source image
        (translate_text if isinstance(translate_text, str) else translate_text[0]).lower(),  # Text
        # tuple(boxes[3]),  # Lower left corner vertex
        (boxes[0][0], boxes[2][1]),  # Lower left corner vertex
        cv2.FONT_HERSHEY_DUPLEX,  # Font codeyarns.com/tech/2015-03-11-fonts-in-opencv.html
        1,  # Font scale
        (0, 0, 0),  # Color
        2  # Line type
    )

cv2.imwrite(f'./assets/result{IMAGE_EXTENSION}', image)
