from google_trans_new import google_translator


translator = google_translator()


def translate(text, language_origin, language_target):
    return translator.translate(
        text,
        lang_src=language_origin,
        lang_tgt=language_target,
    )
