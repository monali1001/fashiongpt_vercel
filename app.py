from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from forms import FashionForm
import google.generativeai as genai
import os


import logging
logging.basicConfig(level=logging.DEBUG)

GOOGLE_API_KEY = 'AIzaSyB-KxlE38SR5ChV_5A7Wxp67VbQvumf8q8'
genai.configure(api_key = GOOGLE_API_KEY)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AIzaSyB-KxlE38SR5ChV_5A7Wxp67VbQvumf8q8'
CORS(app)  # Enable CORS for all routes

@app.route('/ping')
def ping():
    return "pong"


def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def create_prompt(preference, body_type, occasion):
    prompt = f"Please start with a personalized message for someone with a {body_type} body type, including a greeting and a compliment."

    body_type_descriptions = {
        "Rectangle/Straight": "For a rectangle-shaped body type, the key is to create the illusion of curves by defining the waist and adding volume to the bust and hips.",
        "Triangle/Pear": "For a pear-shaped body type, the key is to balance your proportions by highlighting your upper body and drawing attention away from the hips and thighs.",
        "Spoon": "For a spoon-shaped body type, the key is to highlight your waist and upper body while balancing your lower body.",
        "Hourglass": "For an hourglass-shaped body type, the key is to accentuate your waist and highlight your balanced proportions.",
        "Top hourglass": "For a top hourglass-shaped body type, the key is to balance your upper and lower body while highlighting your waist.",
        "Bottom hourglass": "For a bottom hourglass-shaped body type, the key is to balance your lower and upper body while highlighting your waist.",
        "Inverted triangle/Apple": "For an inverted triangle-shaped body type, the key is to balance your broad shoulders with your narrower hips and define your waist.",
        "Round/Oval": "For a round-shaped body type, the key is to elongate your figure and create a defined waist.",
        "Diamond": "For a diamond-shaped body type, the key is to balance your shoulders and hips while defining your waist.",
        "Athletic": "For an athletic-shaped body type, the key is to soften your silhouette by adding feminine curves."
    }

    description = body_type_descriptions.get(body_type, "")
    prompt += f" {description}"

    if preference and occasion:
        prompt += f" Then, provide a cohesive list of fashion recommendations that take into account their preference for {preference} clothing and the occasion of {occasion}. These recommendations should be suitable for a {body_type} body type."
    elif preference:
        prompt += f" Then, provide a list of fashion recommendations based on their preference for {preference}."
    elif occasion:
        prompt += f" Then, provide a list of fashion recommendations for the occasion of {occasion}."
    else:
        prompt += " Then, provide a general list of fashion recommendations."

    prompt += (" Format each recommendation clearly with the item on one line and the description on the next line, separated by a blank line, "
               "and without using asterisks or unnecessary symbols. Use bullet points for each item. Do not include any headers or salutation like 'Personalized Message', 'Fashion Recommendations', 'Dear' ,'Name' or 'Dearest'.")

    return prompt


def format_response(response):
    lines = response.split("\n")
    formatted_lines = []
    for line in lines:
        clean_line = line.strip().lstrip("*-•")
        if clean_line:
            formatted_lines.append(clean_line)
    
    final_output = []
    for i in range(len(formatted_lines)):
        final_output.append(formatted_lines[i])
        if i < len(formatted_lines) - 1 and not formatted_lines[i+1].startswith(" "):
            final_output.append("")
    
    formatted_response = "\n".join(final_output)
    return formatted_response.replace("\n", "<br>")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        preference = request.form.get('preference')
        body_type = request.form.get('body_type')
        occasion = request.form.get('occasion')

        try:
            prompt = create_prompt(preference, body_type, occasion)
            response = get_gemini_response(prompt)
            response = response.replace("*", "")
            print(response)
            return render_template('result.html', recommendations=response)
        except ValueError as e:
            error_message = str(e)
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')  


if __name__ == '__main__':
    app.run(debug=True)