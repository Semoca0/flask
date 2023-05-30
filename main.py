from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
import os
import tempfile

import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})



model = ResNet50(weights='imagenet')

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
#Define the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Specifies the maximum size (in bytes) of the files to be uploaded
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# the web service is created, where we load and identify the data provided by the auxiliary web page
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

            
        if file.filename == '':
            return 'No selected file'
        # We save the image uploaded by the user and proceed to identify it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ruta='/home/XD/Documentos/reconocedor de imagenes/imagenes'
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'],ruta,filename))
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            file.save(temp_file.name)
            img_path = temp_file.name

            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # The image is identified and the data is extracted to show our result on the screen in a user-friendly way
            preds = model.predict(x)
            # decode the results into a list of tuples (class, description, probability)
            # (one such list for each sample in the batch)
            a='Predicted:', decode_predictions(preds, top=1)[0]
            b=''
            c=''
            print(a)
            # print("COMO ESTAS?")
            for i in a[1]:
               b=i[1]
               c=str(int(round(i[2]*100)))
                
            return '''<h2>La Imagen que acabas de Ingresar Corresponde a un '''+b+''' y Estoy un '''+c+'''%  Seguro</h2>'''
        else:
            return 'No allowed extension'
    else 
         return jsonify({"Choo Choo": "Welcome to your Flask app  Jaun🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
