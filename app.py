from __future__ import print_function
import sys
import imghdr
import os
import uuid

# import PIL module
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['DOWNLOAD_PATH'] = 'static/downloads'
app.config['TEMPLATES_AUTO_RELOAD'] = True

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        finname = add_watermark(os.path.join(app.config['UPLOAD_PATH'], filename), filename)
        
        #return render_template('result.html',link=filename)
        #return redirect(url_for('upload_complete', filename=filename))
        #return "valid", 400 
        #return redirect(url_for('upload_complete'))
        print(finname, file=sys.stdout) 
        return render_template('result.html', finname=finname) 
        #return finname
        #return redirect(url_for('upload_files', finname=finname))
        
        
        
    return '', 204
    #return render_template('result.html')


def add_watermark(path, filename):
    # Front Image
    filename_wm = '4ol.png'
    # Back Image
    filename1 = filename
    # Open Front Image
    frontImage = Image.open(os.path.join(app.config['UPLOAD_PATH'], filename_wm))
    # Open Background Image
    background = Image.open(os.path.join(app.config['UPLOAD_PATH'], filename1))
    #resize uploaded image
    background = background.resize((400, 400))
    # Convert image to RGBA
    frontImage = frontImage.convert("RGBA")
    # Convert image to RGBA
    background = background.convert("RGBA")
    # Calculate width to be at the center
    width = (background.width - frontImage.width) // 2
    # Calculate height to be at the center
    height = (background.height - frontImage.height) // 2
    # Paste the frontImage at (width, height)
    background.paste(frontImage, (width, height), frontImage)
    #create random str for filename
    finname = "NETSLEVEL-PFP-" + uuid.uuid4().hex + ".png"
    # Save this image
    background.save(os.path.join(app.config['DOWNLOAD_PATH'], finname), format="png")
    #file name path process
    #finname = secure_filename(finname.filename)
    #return redirect(url_for('uploaded_file', filename=finname))
    #return redirect(url_for('finname'))
    #eturn redirect(url_for('upload_complete', filename='hi'))
    return finname
    

@app.route('/upload-complete')
def upload_complete():
    target = os.path.join(app.config['DOWNLOAD_PATH'], 'downloads/')
    #if request.method == 'POST':
    #return render_template('result.html')
    #print(finname, file=sys.stdout) 
    return render_template('result.html')
    #return redirect(url_for('upload_complete'))   

    