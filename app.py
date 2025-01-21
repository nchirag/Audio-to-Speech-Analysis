from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import speech_recognition as sr
import pickle
import os
from pydub import AudioSegment
#installed ffmpeg using brew install ffmpeg

# Initialize Flask app
# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Load the pre-trained emotion model
with open('/Users/chiragn/Documents/CDAC/Project/speech_emotion_analysis/models/Emotion_classification_model.pkl', 'rb') as file:
    emotion_model = pickle.load(file)
    print("Emotion model loaded successfully")

# Define the database model
class EmotionAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(50), nullable=False)

# Ensure database tables are created
with app.app_context():
    db.create_all()

def convert_audio_to_text(audio_path):
    """Convert audio to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    try:
        # Convert audio to PCM WAV format
        audio = AudioSegment.from_file(audio_path)
        pcm_wav_path = audio_path.replace('.wav', '_pcm.wav')
        audio.export(pcm_wav_path, format='wav')
        print(f"Converted audio to PCM WAV format: {pcm_wav_path}")

        # Use SpeechRecognition to convert audio to text
        with sr.AudioFile(pcm_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error converting audio to text: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Ensure the upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Created directory: {app.config['UPLOAD_FOLDER']}")

    # Save the uploaded audio file
    audio_file = request.files['audio']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'live_audio.wav')
    audio_file.save(file_path)
    print(f"Audio file saved to {file_path}")

    # Check if the file was saved correctly
    if not os.path.exists(file_path):
        print(f"Failed to save audio file to {file_path}")
        return jsonify({'error': 'Failed to save audio file'})

    # Convert audio to text
    text = convert_audio_to_text(file_path)
    if not text:
        print("Failed to convert audio to text")
        return jsonify({'error': 'Failed to process audio'})

    print(f"Converted text: {text}")
    print(f"Type of text: {type(text)}")

    # Predict emotion using the model
    try:
        print(f"Text to be predicted: {text}")
        emotion = emotion_model.predict([text])[0]
        print(f"Predicted emotion: {emotion}")
    except Exception as e:
        print(f"Error predicting emotion: {e}")
        return jsonify({'error': 'Failed to predict emotion'})

    # Save results to the database
    analysis = EmotionAnalysis(text=text, emotion=emotion)
    db.session.add(analysis)
    db.session.commit()

    return jsonify({'text': text, 'emotion': emotion})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
