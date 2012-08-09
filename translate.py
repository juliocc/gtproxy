import json
import requests

GOOGLE_TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2'
GOOGLE_TRANSLATE_KEY = 'AIzaSyCgl2cikF18bXZO5MmzQdGq1z5EZjNZ6M8'
 
def google_translate(text, sl='en', tl='es'):
    """Translates a given text from source language (sl) to target
    language (tl)
    """
    req = requests.get(GOOGLE_TRANSLATE_URL, params={
        'key': GOOGLE_TRANSLATE_KEY,
        'q': text,
        'source': sl,
        'target': tl
    })
    try:
        return json.loads(req.text)['data']['translations'][0]['translatedText']
    except KeyError:
        return None
