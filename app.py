__author__ = 'Nii Odenkey'
import os
from flask import Flask, jsonify, render_template, request
from keras.metrics import top_k_categorical_accuracy, categorical_accuracy
import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)

def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)

model = load_model("model_diagnosify_app.h5", custom_objects={"top_2_accuracy": top_2_accuracy, "top_3_accuracy": top_3_accuracy}, compile=False)
model._make_predict_function()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    return render_template('diagnose.html')


@app.route('/predict', methods=['POST'])
def predict():
    def top_3_accuracy(y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=3)

    def top_2_accuracy(y_true, y_pred):
        return top_k_categorical_accuracy(y_true, y_pred, k=2)

    print(APP_ROOT)
    target = '/'.join([APP_ROOT, 'images'])
    print(target)

    for file in request.files.getlist("scanImage"):
        print('got here!!!!!')
        print(file)
        filename = file.filename
        destination = '/'.join([target, filename])
        print(destination)
        file.save(destination)

        test_image = image.load_img(destination)
        test_image = image.img_to_array(test_image)
        test_image = cv2.resize(test_image, (224, 224))
        print(test_image.dtype)
        print(test_image.shape)

        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        labels = ['akiec', 'bcc', 'bk1', 'df', 'mel', 'nv', 'vasc']
        print(result)
        indexes = np.argmax(result, axis=-1)
        encoded_result = [labels[i] for i in indexes]
        if encoded_result[0] == "akiec":
            output = "Actinic Keratoses"
            info = """An actinic keratosis (ak-TIN-ik ker-uh-TOE-sis) is a rough, 
            scaly patch on your skin that develops from years of exposure to the sun. 
            It's most commonly found on your face, lips, ears, back of your hands, forearms, 
            scalp or neck."""
            ref = "https://www.mayoclinic.org/diseases-conditions/actinic-keratosis/symptoms-causes/syc-20354969"
        elif encoded_result[0] == "bcc":
            output = "Basal cell carcinoma"
            info = """Basal cell carcinoma is a type of skin cancer. 
            Basal cell carcinoma begins in the basal cells — a type of cell within the skin that 
            produces new skin cells as old ones die off."""
            ref = "https://www.mayoclinic.org/diseases-conditions/basal-cell-carcinoma/symptoms-causes/syc-20354187"
        elif encoded_result[0] == "bk1":
            output = "Benign keratosis"
            info = """A seborrheic keratosis (seb-o-REE-ik ker-uh-TOE-sis) is a common noncancerous 
            skin growth. People tend to get more of them as they get older. Seborrheic keratoses are 
            usually brown, black or light tan. The growths look waxy, scaly and slightly raised."""
            ref = "https://www.mayoclinic.org/diseases-conditions/seborrheic-keratosis/symptoms-causes/syc-20353878"
        elif encoded_result[0] == "df":
            output = "Dermatofibroma"
            info = """Dermatofibrosarcoma protuberans (DFSP) is a very rare type of skin cancer that begins in
             connective tissue cells in the middle layer of your skin (dermis).Dermatofibrosarcoma 
             protuberans may at first appear as a bruise or scar. As it grows, lumps of tissue 
             (protuberans) may form near the surface of the skin."""
            ref = "https://www.mayoclinic.org/diseases-conditions/dermatofibrosarcoma-protuberans/cdc-20352949"
        elif encoded_result[0] == "nv":
            output = "Melanocytic nevi"
            info = """ Melanocytic nevi are benign neoplasms or hamartomas composed of melanocytes, 
            the pigment-producing cells that constitutively colonize the epidermis. 
            Melanocytes are derived from the neural crest and migrate during embryogenesis to selected 
            ectodermal sites (primarily the skin and the CNS), but also to the eyes and the ears."""
            ref = "https://emedicine.medscape.com/article/1058445-overview"
        elif encoded_result[0] == "mel":
            output = "Melanoma"
            info = """Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) 
            that produce melanin — the pigment that gives your skin its color. Melanoma can also form in 
            your eyes and, rarely, in internal organs, such as your intestines."""
            ref = "https://www.mayoclinic.org/diseases-conditions/melanoma/symptoms-causes/syc-20374884"
        elif encoded_result[0] == "vasc":
            output = "Vascular skin lesions"
            info = """Vascular lesions are relatively common abnormalities of the skin and underlying 
            tissues, more commonly known as birthmarks. There are three major categories of vascular 
            lesions: Hemangiomas, Vascular Malformations, and Pyogenic Granulomas."""
            info = "https://www.ssmhealth.com/cardinal-glennon/pediatric-plastic-reconstructive-surgery/hemangiomas"
        else: 
            output = "No result"
            info = "Get more info at "
            ref = "https://www.healthline.com/health/skin-disorders"
    return render_template('prediction.html', prediction_text="You likely have {}".format(output), info = info, ref = ref)

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')
    
if __name__ == '__main__':
    app.run(port=4555, debug=True)
