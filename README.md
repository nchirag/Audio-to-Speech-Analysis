# Speech Emotion Analysis by Chirag N

This project is a web application that allows users to analyze the emotion in speech. Users must sign up and log in to use the application. The application uses Flask for the web framework, SQLAlchemy for the database, and various libraries for audio processing and emotion prediction.

## Features

- Upload audio files for emotion analysis
- Convert audio to text using SpeechRecognition
- Predict emotion from text using a pre-trained model
- Store analysis results in a database

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/speech_emotion_analysis.git
    cd speech_emotion_analysis
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Install `ffmpeg` (required for audio processing):
    ```sh
    brew install ffmpeg
    ```

5. Set up the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Sign up for a new account or log in with an existing account.

4. Upload an audio file and click "Analyze" to get the emotion analysis.

## File Structure

- [app.py](http://_vscodecontentref_/0): Main application file
- `models.py`: Database models
- `forms.py`: Forms for user authentication
- [templates](http://_vscodecontentref_/1): HTML templates
  - `signup.html`: Sign-up page
  - `login.html`: Login page
  - [index.html](http://_vscodecontentref_/2): Main application page
- [static](http://_vscodecontentref_/3): Static files (CSS, JavaScript, etc.)
- [requirements.txt](http://_vscodecontentref_/4): List of required packages

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
