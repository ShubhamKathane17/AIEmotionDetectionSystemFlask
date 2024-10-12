"""
Emotion Detection Server Module.

This module creates a Flask application that detects emotions in user-provided text using 
the emotion_detector function. The web application serves an input page and processes 
emotion analysis via the /emotionDetector endpoint.
"""

import requests
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Initialize the Flask application
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_detector_function():
    """
    Endpoint to analyze the emotion of the given text input.
    Returns the emotion analysis result or an error message.
    """
    # Get the text from the query parameters
    text_to_analyze = request.args.get('textToAnalyze')

    # Validate the input text
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid Input! Please provide a valid text for analysis."

    try:
        # Call the emotion detection function
        response = emotion_detector(text_to_analyze)

        # Check if the response contains a valid dominant emotion
        if response['dominant_emotion'] is None:
            response_text = "Invalid Input! Please try again."
        else:
            # Format the response text while maintaining line length constraints
            response_text = (
                f"For the given statement, the system response is:\n"
                f"'Anger': {response['anger']}, 'Disgust': {response['disgust']},\n"
                f"'Fear': {response['fear']}, 'Joy': {response['joy']},\n"
                f"'Sadness': {response['sadness']}.\n"
                f"The dominant emotion is: {response['dominant_emotion']}."
            )
    except requests.exceptions.RequestException as e:
        # Handle network-related errors specifically
        return f"An error occurred during the request: {str(e)}"
    except KeyError as e:
        # Handle errors related to missing keys in the response
        return f"Unexpected response format: Missing key {str(e)}"
    except Exception as e:
        # Handle unexpected errors while being more specific
        return f"An unexpected error occurred: {str(e)}"

    return response_text


@app.route("/")
def render_index_page():
    """Renders the main index page for input."""
    return render_template('index.html')


if __name__ == "__main__":
    # Start the Flask application
    app.run(host="0.0.0.0", port=5000)
