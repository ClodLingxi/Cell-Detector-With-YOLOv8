import cv2
import os
from label_studio_sdk import Client


def insert_label_studio(url, api_key, pic_path='./output_blocks/'):

    if url == '':
        LABEL_STUDIO_URL = 'http://localhost:8080'
    else:
        LABEL_STUDIO_URL = url

    API_KEY = api_key  # Label Studio API

    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    project = ls.get_project(5)

    for i in range(12):

        image = cv2.imread(pic_path + f"block_{i}.jpg")
        height, width, channels = image.shape

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        file_path = 'labels/' + os.path.basename(pic_path) + '.json'
        folder_path = os.path.dirname(file_path)

        if not os.path.exists(file_path):
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        count = 0

        result = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            s = abs(w * h)
            if s < 100 or s > 3000:
                continue

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            result.append({
                "id": "result" + str(count),
                "type": "rectanglelabels",
                "from_name": "label",
                "to_name": "image",
                "original_width": width,
                "original_height": height,
                "image_rotation": 0,
                "value": {
                    "rotation": 0,
                    "x": x / width * 100,
                    "y": y / height * 100,
                    "width": w / width * 100,
                    "height": h / height * 100,
                    "rectanglelabels": ["Cell"]
                }
            })

            count += 1

        data = [{
            "data": {
                "image": f"/data/local-files/?d=output_blocks%5Cblock_{i}.jpg"
            },
            "predictions": [{
                "model_version": "one",
                "score": 1,
                "result": result
            }]
        }]

        project.import_tasks(data)
