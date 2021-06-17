import requests

def search(fn):
    image_data = None
    with open(fn, "rb") as f:
        image_data = f.read()

    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    ocr_url = vision_base_url + "analyze"
    subscription_key = '' # Azure Subscription key
    assert subscription_key
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color,Tags'}
    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    ds = response.json()
    text=ds['tags']

    tags=[]
    for i in text:
        if float(i['confidence'])>=0.50:
            tags.append(i['name'])
    return tags


def search_desc(fn):
    image_data = None
    with open(fn, "rb") as f:
        image_data = f.read()

    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    ocr_url = vision_base_url + "analyze"
    subscription_key = ''
    assert subscription_key
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color,Tags'}
    response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    ds = response.json()
    text=ds['description']
    if len(text['captions']) > 0:
        txt = text['captions'][0]
        return txt['text']
    else:
        return "Nothing found"


def ocr(file_location):
    with open(file_location, 'rb') as file:
        image_data = file.read()
    payload = {
        'isOverlayRequired':False,
        'apikey': '', # OCR Space API key here
        'filetype': 'JPG'
    }
    response = requests.post('https://api.ocr.space/parse/image',
                             files={'filename': image_data},
                             data=payload)
    response.raise_for_status()
    return response.json()['ParsedResults'][0]['ParsedText']


def ocr_azure(file_location):
    with open(file_location, 'rb') as file:
        image_data = file.read()
    endpoint = 'westcentralus.api.cognitive.microsoft.com'
    url = f'https://{endpoint}/vision/v3.1/ocr?language=en&detectOrientation=true'
    subscription_key = ''
    assert subscription_key
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()
    words = []
    for boundingBox in response.json()['regions']:
        for line in boundingBox['lines']:
            for word in line['words']:
                if word['text'].isalpha():
                    words.append(word['text'])
    return ' '.join(words)

