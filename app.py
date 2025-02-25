from flask import *
import os

app = Flask(__name__)
app.secret_key = 'test'

UPLOAD_FOLDER = 'uploads' #Directory to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok =True) #makes the uploads directory if it doesn't already exist

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

#this function takes the filename, checks for a '.' and splits the name at the final '.' to check if its extension matches an item from the ALLOWED_EXTENSIONS set
def check_file_eligibility(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#this allows the html file to extract the files from downloads
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory('uploads', filename)

#directs anyone who arrives at the home URL to execute the index function
@app.route('/')
def index():
    #Get list of audio files in the uploads directory
    audio_files = []
    if os.path.exists(UPLOAD_FOLDER):
        audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if check_file_eligibility(f)]
    #this sends the audio_files list to the html template
    return render_template('index.html', audio_files=audio_files)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if request.method == 'POST':
        if 'fileUp' not in request.files:
            return render_template('results.html', msg="No file part")

        fileitem = request.files['fileUp']

        if fileitem.filename == '':
            return render_template('results.html', msg="No file selected")

        if fileitem and check_file_eligibility(fileitem.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], fileitem.filename)
            fileitem.save(filepath)

            return redirect(url_for('index'))
        else:
            return render_template('results.html', msg="File type not allowed. Please upload .mp3 or .wav files only.")

@app.route('/vocal')
def vocal_separation():
  return "Vocal separation feature coming soon"

#runs the app
if __name__ == '__main__':
  app.run(debug=True, port=5001) #this runs the app with debug mode active