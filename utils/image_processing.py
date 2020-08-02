import numpy as np
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image
from keras.models import load_model
import urllib.request
import os


def predict(model, img):
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds[0]


def category_predict(imgs):
    j = 0
    predictions = list()
    context = dict()
    model = load_model('filename.model')
    for i in imgs:
        try:
            urllib.request.urlretrieve( i, f"static/temp/cache_{j}.jpg")
            print("success")
            img = image.load_img(f'static/temp/cache_{j}.jpg', target_size=(300, 300))
            preds = predict(model, img)
            context[str(i)] = list(preds)
            print(f"done{j}")
            j += 1
        except:
            print("failed")
            j += 1
            continue

    print("done all")
    return context