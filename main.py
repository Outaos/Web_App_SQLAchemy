from io import BytesIO

from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy 

# Create a Flask app
app = Flask(__name__)
# Establish a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.debug = True
# Create a database object which will connect database to the app
db = SQLAlchemy(app)

# A function to create all necessary tables for the application.
# It is called without any arguments and its return value is ignored.
@app.before_first_request
def create_tables():
    db.create_all()
    
# Establish a class for a table and create SQLAlchemy model
class Upload(db.Model):
    # Create table columns, specify data type
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    story = db.Column(db.String(50))
    lng = db.Column(db.Float)                   
    lat = db.Column(db.Float)                   

# Create routes and connect them to relevant HTML files
@app.route('/home')
def home():
    return render_template('./home.html')

@app.route('/play')
def play():
    return render_template('./play.html')

@app.route('/manchester')
def manchester():
    return render_template('./manchester.html')

@app.route('/ternopil')
def ternopil():
    return render_template('./ternopil.html')

@app.route('/beijing')
def beijing():
    return render_template('./beijing.html')

@app.route('/storieste')
def storieste():
    return render_template('./storiesTe.html')

@app.route('/storiesbe')
def storiesbe():
    return render_template('./storiesBe.html')

@app.route('/art')
def art():
    return render_template('./art.html')

@app.route('/stories')
def stories():
    return render_template('./stories.html')

@app.route('/', methods=['GET', 'POST'])
def create():
    # Take the file from the form
    if request.method == 'POST':
        file = request.files['file']
        add_story = request.form['story']  
        add_lng = request.form['insert_longitude']    
        add_lat = request.form['insert_latitude']    

        # Add the file and coords info to the database
        upload = Upload(filename=file.filename, data=file.read(), story=add_story, lng=add_lng, lat=add_lat) 
        db.session.add(upload)
        db.session.commit()

        # Notify the user that the file has been uploaded
        return f'Uploaded: {file.filename}. Please reload the page.'
    return render_template('./create.html')

# Create a route to retrive the data
@app.route('/download/<upload_id>')
def download(upload_id):
    # Perform a query to select a file with stated ID
    upload = Upload.query.filter_by(id=upload_id).first()
    # Convert a binary data to a format Flask can use to regenerate the file, and return this file
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)

