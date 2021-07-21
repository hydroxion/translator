import easyocr

import cv2

from .language import translate

from .utils import grouper


def ocr(image, language_origin, paragraph):
    reader = easyocr.Reader([language_origin])

    return reader.readtext(image, paragraph=paragraph)


def photoshop(image, image_ocr, paragraph, language_target, group_size):
    for sentence in image_ocr:
        boxes, text, confident = [*sentence, None] if paragraph else sentence

        cv2.rectangle(
            image,
            tuple(boxes[0]),
            (boxes[1][0], boxes[2][1]),
            (255, 255, 255),
            -1,
        )

        translated_text = translate(text, language_target)

        box_text = (
            translated_text
            if isinstance(translated_text, str) else
            translated_text[0]
        ).capitalize()

        box_text_groups = list(grouper(box_text.split(), group_size))

        x = boxes[0][0] # - 20

        y = boxes[2][1] # - 60

        for box_text_group in box_text_groups:
            cv2.putText(
                image,
                ' '.join(filter(lambda word: word, box_text_group)),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,  # FONT_HERSHEY_SIMPLEX
                .75,
                (0, 0, 0),
                1
            )

            y += 30

    return image
