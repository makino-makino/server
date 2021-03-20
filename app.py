import os
import io
import time
import json
import numpy as np
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'PNG', 'JPG'])
IMAGE_WIDTH = 640
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/img', methods=['GET', 'POST'])
def img():
    if request.method == 'POST':
        data = request.json['img']
        npimg = np.fromstring(data, dtype=np.uint8); 
        source = cv2.imdecode(npimg, 1)

        image = cv2.imread(source)

        image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")


        face_list=cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=2,minSize=(64,64))

        if len(face_list) > 0:
            for rect in face_list:
                x,y,width,height=rect
                image = image[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
                if image.shape[0]<64:
                    continue
                image = cv2.resize(image,(64,64))

                fileName=os.path.join(out_dir + names[i],str(num)+".jpg")
                cv2.imwrite(str(fileName),image)
                print(str(num)+".jpgを保存しました.")
                return("OK")
        else:
            print("no face")
            return("no face")
        return(data)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']

        # 変なファイル弾き
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
        else:
            return ''' <p>許可されていない拡張子です</p> '''

        # BytesIOで読み込んでOpenCVで扱える型にする
        f = img_file.stream.read()
        bin_data = io.BytesIO(f)
        file_bytes = np.asarray(bytearray(bin_data.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # とりあえずサイズは小さくする
        raw_img = cv2.resize(img, (IMAGE_WIDTH, int(IMAGE_WIDTH*img.shape[0]/img.shape[1])))

        # サイズだけ変えたものも保存する
        raw_img_url = os.path.join(app.config['UPLOAD_FOLDER'], 'raw_'+filename)

        # なにがしかの加工
        gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

        # 加工したものを保存する
        gray_img_url = os.path.join(app.config['UPLOAD_FOLDER'], 'gray_'+filename)
        cv2.imwrite(gray_img_url, gray_img)

        print(gray_img_url, raw_img_url)
        return render_template('index.html', raw_img_url=raw_img_url, gray_img_url=gray_img_url)

    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.debug = True
    app.run(
        host="0.0.0.0",
        port=5000)
