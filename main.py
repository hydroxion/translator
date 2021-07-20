from source.scripts.image import ocr, photoshop

import cv2


image = cv2.imread('./assets/images/test.jpg')

language_origin = 'en'

language_target = 'pt'

paragraph = False

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
    language_target=language_target,
    group_size=2
)

cv2.imwrite(f'./assets/images/result.jpg', image_photoshop)
