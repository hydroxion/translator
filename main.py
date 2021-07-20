import easyocr

from google_trans_new import google_translator

from transformers import AutoTokenizer, AutoModelForCausalLM

import torch

import cv2


translator = google_translator()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained('salesken/grammar_correction')

model = AutoModelForCausalLM.from_pretrained(
    'salesken/grammar_correction'
).to(device)


def ocr(image, language_origin, paragraph):
    reader = easyocr.Reader([language_origin])

    return reader.readtext(image, paragraph=paragraph)


def translate(text, language_origin, language_target):
    return translator.translate(
        text,
        lang_src=language_origin,
        lang_tgt=language_target,
    )


def grammar_correction(text):
    query = "<|startoftext|> " + text  # '~~~'

    input_ids = tokenizer.encode(query.lower(), return_tensors='pt').to(device)

    sample_output = model.generate(
        input_ids,
        do_sample=True,
        num_beams=1,
        max_length=128,
        temperature=0.9,
        top_p=0.85,
        top_k=5,
        num_return_sequences=1
    )

    return tokenizer.decode(sample_output[0], skip_special_tokens=True).split('||')[0].split('~~~')[1]


def photoshop(image, image_ocr, language_origin, paragraph, language_target):
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

        print(box_text)

        cv2.putText(
            image,
            box_text,
            (boxes[0][0], boxes[2][1]),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,  # FONT_HERSHEY_SIMPLEX
            1,
            (0, 0, 0),
            2
        )

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
