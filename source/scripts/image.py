import easyocr

import cv2

from .language import translate

from .utils import grouper


def ocr(image, language_origin, paragraph):
    reader = easyocr.Reader([language_origin])

    return reader.readtext(image, paragraph=paragraph)


def photoshop(image, image_ocr, language_origin, paragraph, language_target, group_size):
    # Revert paint to avoid overlap
    for sentence in reversed(image_ocr):
        boxes, text, confident = [*sentence, None] if paragraph else sentence

        cv2.rectangle(
            image,
            tuple(boxes[0]),
            (boxes[1][0], boxes[2][1]),
            (255, 255, 255),
            -1,
        )

        translate_text = translate(text, language_origin, language_target)

        box_text = (
            translate_text
            if isinstance(translate_text, str) else
            translate_text[0]
        ).capitalize()

        box_text_groups = list(grouper(box_text.split(), group_size))

        x = boxes[0][0] - 20

        y = boxes[2][1] - 60

        for box_text_group in box_text_groups:
            cv2.putText(
                image,
                ' '.join(filter(lambda word: word, box_text_group)),
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,  # FONT_HERSHEY_SIMPLEX
                1,
                (0, 0, 0),
                2
            )

            y += 30

    return image
