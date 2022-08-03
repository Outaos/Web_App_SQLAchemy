from io import BytesIO

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.debug = True
db = SQLAlchemy(app)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    story = db.Column(db.String(50))
    lng = db.Column(db.Float)                   # String(50)
    lat = db.Column(db.Float)                    # String(50)


#@app.route("/")
#def base():
    #return render_template('./base.html')   # index page

@app.route('/home')
def home():
    return render_template('./home.html')

@app.route('/art')
def art():
    return render_template('./art.html')

@app.route('/stories')
def stories():
    return render_template('./stories.html')

@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        file = request.files['file']
        add_story = request.form['story']   #args
        add_lng = request.form['insert_longitude']    #args   lng = float(request.args['lng'])
        add_lat = request.form['insert_latitude']    #args   lat = float(request.args['lat']) 


        upload = Upload(filename=file.filename, data=file.read(), story=add_story, lng=add_lng, lat=add_lat)      #
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}. Please reload the page.'
    return render_template('./create.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)

# without this code I get "sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: upload" Error
@app.before_first_request
def create_tables():
    db.create_all()

    # upload = Upload(filename=file.filename, data=file.read(), name=the_name)
