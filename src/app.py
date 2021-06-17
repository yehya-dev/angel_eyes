import flask
import time
from src.database import select,iud,selectall,selecte

app = flask.Flask(__name__)

# app.secret_key = '' 
# Secret key can be created using 
# import os
# os.urandom(24)

@app.route('/adminhome')
def adminhome():
    if 'aid' in flask.session:
        return flask.render_template('adminhome.html')
    else:
        return '''<script>alert('Admin Only Page');window.location='/'</script>'''

@app.route('/')
def main():
    flask.session.clear()
    return flask.render_template('login.html')


@app.route('/login',methods=['post'])
def login():
    username=flask.request.form['username']
    password = flask.request.form['password']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password`=%s"
    val=(username,password)
    res=select(qry,val)
    if res is None:
        return '''<script>alert('Invalid username or password');window.location='/'</script>'''
    else:

        if res[3]=='admin':
            flask.session['aid'] = res[0]
            return '''<script>window.location='/adminhome'</script>'''
        else:
            flask.session['id'] = res[0]
            return '''<script>window.location='/caretakerhome'</script>'''

@app.route('/viewcaretaker')
def viewcaretaker():
    if 'aid' in flask.session:
        qry = "SELECT * from `caretaker`"
        res = selectall(qry)
        return flask.render_template('viewcaretaker.html',val=res)
    else:
        return '''<script>alert('Admin Only Page');window.location='/'</script>'''


@app.route('/viewreview')
def viewreview():
    if 'aid' in flask.session:
        qry = 'SELECT * FROM `review` JOIN `caretaker` ON caretaker.caretaker_id = review.caretaker_id'
        res = selectall(qry)
        return flask.render_template('viewreview.html', val=res)
    else:
        return '''<script>alert('Admin Only Page');window.location='/'</script>'''

@app.route('/addblind')
def addblind():
    if 'id' in flask.session:
        return flask.render_template('addblind.html')
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''


@app.route('/createblind', methods=['POST'])
def createblind():
    if 'id' in flask.session:
        name = flask.request.form.get('name')
        age = flask.request.form.get('age')
        gender = flask.request.form.get('gender')
        place = flask.request.form.get('place')
        phone = flask.request.form.get('phone')
        pin = flask.request.form.get('pin')
        post = flask.request.form.get('post')
        imei = flask.request.form.get('imei')
        id = flask.session['id']
        qry = 'INSERT INTO `blind` VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (str(id), name, str(age), phone, gender, place, pin, post, imei)
        bid=iud(qry, val)
        qry="insert into location values(null,%s,%s,%s)"
        val=(str(bid),"11.67","74.567")
        iud(qry, val)
        return '''<script>alert('Registered succesfully');window.location='/viewblind'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''


@app.route('/addfeedback')
def addfeedback():
    if 'id' in flask.session:
        return flask.render_template('addfeedback.html')
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/createfeedback', methods=['POST'])
def createfeedback():
    if 'id' in flask.session:
        review = flask.request.form.get('feedback')
        id = flask.session.get('id')
        qry = 'SELECT `caretaker`.`caretaker_id` FROM `caretaker` JOIN `login` ON `caretaker`.`login_id` = `login`.`login_id` WHERE `caretaker`.`login_id`=%s'
        caretaker_id = select(qry, str(id))
        qry = 'INSERT INTO `review` VALUES (NULL, %s, %s, curdate(), curtime())'
        val = (caretaker_id, review)
        iud(qry, val)
        return '''<script>alert('Feedback added succesfully');window.location='/caretakerreviews'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/caretakerhome')
def caretakerhome():
    if 'id' in flask.session:
        return flask.render_template('caretakerhome.html')
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/caretakerreviews')
def caretakerreviews():
    if 'id' in flask.session:
        id = flask.session.get('id')
        qry = 'SELECT `caretaker_id` FROM `caretaker` WHERE `login_id` = %s'
        caretaker_id = select(qry, str(id))
        qry = 'SELECT review_id,review,date FROM `review` WHERE `caretaker_id`=%s'
        res = selecte(qry, str(caretaker_id[0]))
        return flask.render_template('caretakerreviews.html', val=res)
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''


@app.route('/notificationview')
def notificationview():
    return flask.render_template('notificationview.html')

@app.route('/register')
def register():
    return flask.render_template('register.html')

@app.route('/viewblindadmin')
def viewblindadmin():
    if 'aid' in flask.session:
        id = flask.request.args.get('id')
        qry = "SELECT `blind`.*,`location`.`latitude`,`location`.`longitude` FROM `blind` JOIN `location` ON `location`.`blind_id`=`blind`.`blind_id` WHERE `blind`.`caretaker_id`=%s"
        res = selecte(qry, id)
        return flask.render_template('viewblindadmin.html', val=res)
    else:
        return '''<script>alert('Admin Only Page');window.location='/'</script>'''

@app.route('/createcaretaker', methods=["POST"])
def createcaretaker():
    name = flask.request.form.get('name')
    age = flask.request.form.get('age')
    district = flask.request.form.get('district')
    place = flask.request.form.get('place')
    pin = flask.request.form.get('pin')
    post = flask.request.form.get('post')
    phone = "91" + flask.request.form.get('phone')
    email = flask.request.form.get('email')
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    gender = flask.request.form.get('gender')
    qry = "INSERT INTO `login` VALUES (NULL, %s, %s, 'caretaker')"
    val = (username, password)
    id = iud(qry, val)
    qry = "INSERT INTO `caretaker` VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, name, phone, age, gender, email, district, pin, place, post)
    iud(qry, val)
    return '''<script>window.location='/'</script>'''

@app.route('/viewblind')
def viewblind():
    if 'id' in flask.session:
        id=flask.session['id']
        qry = "SELECT `blind`.*,`location`.`latitude`,`location`.`longitude` FROM `blind` JOIN `location` ON `location`.`blind_id`=`blind`.`blind_id` WHERE `blind`.`caretaker_id`=%s"
        value=str(id)
        res = selecte(qry, value)
        return flask.render_template('viewblind.html', val=res)
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/editblind')
def editblind():
    if 'id' in flask.session:
        bid = flask.request.args.get('id')
        qry = 'SELECT name, age, phone, gender, place, pin, post, imei FROM blind WHERE blind_id=%s'
        val = (str(bid),)
        res = select(qry, val)
        return flask.render_template('editblind.html', blind=bid, res=res)
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/updateblind', methods=['POST'])
def updateblind():
    if 'id' in flask.session:
        print(flask.request.form)
        bid = flask.request.form.get('blindid')
        name = flask.request.form.get('name')
        age = flask.request.form.get('age')
        gender = flask.request.form.get('gender')
        place = flask.request.form.get('place')
        pin = flask.request.form.get('pin')
        phone = flask.request.form.get('phone')
        post = flask.request.form.get('post')
        imei = flask.request.form.get('imei')
        qry = 'UPDATE `blind` SET name=%s, age=%s, phone=%s, gender=%s, place=%s, pin=%s, post=%s, imei=%s WHERE `blind_id`=%s'
        val = (name, str(age), str(phone), gender, place, pin, post, imei, str(bid))
        iud(qry, val)
        return f'''<script>alert('Updated Successfully');window.location='/viewblind'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/knownpeople')
def knownpeople():
    if 'id' in flask.session:
        id = flask.request.args.get('id')
        qry = "SELECT * FROM `face` WHERE bid=%s"
        value = str(id)
        res = selecte(qry, value)
        return  flask.render_template('knownlist.html', blind=id, res=res)

@app.route('/addknownview')
def addknownview():
    if 'id' in flask.session:
        blind = flask.request.args.get('id')
        print(blind)
        return flask.render_template('addknownview.html', blind=blind)

@app.route('/addknown', methods=['POST'])
def addknown():
    if 'id' in flask.session:
        name = flask.request.form.get('personName')
        blind = flask.request.form.get('blind')
        photo = flask.request.files.get('photo')
        file_ext = photo.filename.split('.')[-1]
        image_path = f'{int(time.time())}.{file_ext}'
        save_loc = f'./static/face/{image_path}'
        photo.save(save_loc)
        qry = "INSERT INTO `face` values (NULL, %s, %s, %s)"
        val = (str(blind), name, save_loc)
        id = iud(qry, val)
        return f'''<script>window.location='/knownpeople?id={blind}'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/deleteknown', methods=['GET'])
def deleteknown():
    if 'id' in flask.session:
        pers_id = flask.request.args.get('id')
        blind_id = flask.request.args.get('blind')
        qry = 'DELETE FROM `face` WHERE id=%s'
        val = str(pers_id)
        iud(qry, val)
        return f'''<script>window.location='/knownpeople?id={blind_id}'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''


@app.route('/deleteblind')
def deleteblind():
    if 'id' in flask.session:
        id = flask.request.args.get('id')
        qry = 'DELETE FROM `blind` WHERE blind_id=%s'
        iud(qry, id)
        return '''<script>alert('Successfully Delelted');window.location='/viewblind'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/deletefeedback')
def deletefeedback():
    if 'id' in flask.session:
        id = flask.request.args.get('id')
        qry = 'DELETE FROM `review` WHERE `review_id` = %s'
        iud(qry, str(id))
        return '''<script>alert('Deleted Feedback Successfully');window.location='/caretakerreviews'</script>'''
    else:
        return '''<script>alert('Caretaker Only Page');window.location='/'</script>'''

@app.route('/volunteerregister')
def volunteerregister():
    return flask.render_template('volunteerregister.html')

@app.route('/addvolunteer', methods=['POST'])
def addvolunteer():
    name = flask.request.form.get('name')
    place = flask.request.form.get('place')
    post = flask.request.form.get('post')
    email = flask.request.form.get('email')
    phone = flask.request.form.get('phone')
    qry = "INSERT INTO `volunteer` values (NULL, %s, %s, %s, %s, %s, 0)"
    values = (name, place, post, email, phone)
    iud(qry, values)
    return '''<script>alert('Successfully Registered Volunteer');window.location='/'</script>'''

@app.route('/volunteerview')
def volunteerview():
    return flask.render_template('volunteerview.html')

app.run(debug=True)