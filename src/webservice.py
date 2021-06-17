from flask import *
from src.database import select, iud, selectall
from src.apis import ocr_azure
from src.recognize_face import rec_face_image
import cv2
from src.objectdetection import objdet

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

app = Flask(__name__)

@app.route('/updateloc', methods=['POST'])
def updateloc():
    try:
        imei = request.form['imei']
        latt = request.form['latt']
        long = request.form['long']
        qry = 'SELECT `blind_id` FROM `blind` WHERE `imei`=%s'
        res = select(qry, (str(imei),))
        qry = 'UPDATE `location` SET `latitude`=%s, `longitude`=%s WHERE `blind_id`=%s'
        val = (str(latt), str(long), str(res[0]))
        iud(qry, val)
        return jsonify({"task":"ok"})
    except Exception as e:
        print(e)
        return jsonify({"task":"error"})


@app.route('/addemergency', methods=["POST"])
def addemergency():
    try:
        imei = request.form['imei']
        latt = request.form['latt']
        long = request.form['longi']
        qry = 'SELECT `blind_id` FROM `blind` WHERE `imei`=%s'
        res = select(qry, (str(imei),))
        qry = 'INSERT INTO `emergency` VALUES(NULL, %s, %s, %s, CURDATE(), CURTIME())'
        val = (str(res[0]), str(latt), str(long))
        iud(qry, val)
        return  jsonify({'task': 'ok'})
    except Exception as e:
        print(e)
        return jsonify({'task': 'error'})


@app.route('/capture', methods=["POST"])
def capture():
    try:
        save_location = "static/identify.jpg"
        img = request.files['files']
        imei = request.form['imei']
        img.save(save_location)
        img=cv2.imread(save_location)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(len(faces))
        if len(faces)==0:
            results = objdet(save_location)
            re=', '.join(results)+" are in front of you"

            return jsonify({'task': re})
        else:
            ids=rec_face_image(save_location)
            print(ids)
            ids.append('0')
            fids=','.join(ids)
            qry=f"SELECT NAME FROM `face` WHERE `id` IN ({fids}) AND `bid` IN(SELECT `blind_id` FROM `blind` WHERE `imei`='{imei}')"
            print(qry)
            s=selectall(qry)
            if s is None:
                return jsonify({'task': " person is infront of you"})
            print(s)
            return jsonify({'task':" "+s[0][0]+" is infront of you"})
    except Exception as e:
        print(e)
        return jsonify({'task': "false"})


@app.route('/ocr', methods=["POST"])
def ocr():
    try:
        file_location = './static/ocr.jpeg'
        img = request.files['files']
        img.save(file_location)
        result_text = ocr_azure(file_location)
        return jsonify({'task': result_text})
    except Exception as e:
        print(e)
        return jsonify({'task': 'error'})

@app.route('/getphone', methods=["POST"])
def getPhone():
    try:
        imei = request.form['imei']
        qry = 'SELECT `caretaker`.`contact`, `blind`.`name` FROM `blind` JOIN `caretaker` ON `blind`.`caretaker_id` = `caretaker`.`login_id` WHERE `blind`.`imei`= %s'
        res = select(qry, (str(imei),))
        return jsonify({'status': 'ok', 'contact': str(res[0]), 'bname':res[1]})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error'})


@app.route('/getvolphone', methods=['GET'])
def getvolphone():
    qry = 'SELECT `phno` FROM `volunteer` ORDER BY `point` DESC'
    res = selectall(qry)
    volPhone = res[0][0]
    return jsonify({
        'volphone': volPhone
    })


app.run(host='0.0.0.0',port=5000)
