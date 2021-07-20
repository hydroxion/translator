import easyocr

from google_trans_new import google_translator

from itertools import zip_longest

import cv2


translator = google_translator()


def ocr(image, language_origin, paragraph):
    reader = easyocr.Reader([language_origin])

    return reader.readtext(image, paragraph=paragraph)


def translate(text, language_origin, language_target):
    return translator.translate(
        text,
        lang_src=language_origin,
        lang_tgt=language_target,
    )


def grouper(iterable, group_size):
    args = [iter(iterable)] * group_size

    return zip_longest(*args)


def photoshop(image, image_ocr, language_origin, paragraph, language_target):
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

        box_text_groups = list(grouper(box_text.split(), 3))

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


if __name__ == '__main__':
    image = cv2.imread('./assets/test.jpg')

    language_origin = 'en'

    language_target = 'pt'

    paragraph = True

    image_ocr = ocr(
        image=image,
        language_origin=language_origin,
        paragraph=paragraph
    )

    image_photoshop = photoshop(
        image=image,
        image_ocr=image_ocr,
        language_origin=language_origin,
        paragraph=paragraph,
        language_target=language_target
    )

    cv2.imwrite(f'./assets/result.jpg', image_photoshop)
