
import os
from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
import re
app = Flask(__name__)

# Temporarily set the API key directly for testing
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('generate_itinerary'))
    return render_template('home.html')

@app.route('/itinerary', methods=['POST'])
def generate_itinerary():
    destination = request.form['destination']
    travel_date = request.form['travel_date']
    vacation_length = request.form['vacation_length']
    number_of_people = request.form['number_of_people']

    # Generate the itinerary using the OpenAI client
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a travel assistant."},
        {"role": "user", "content": f"Create a detailed travel itinerary for a trip to {destination} for {number_of_people} people from {travel_date}, lasting {vacation_length} days."}
      ]
    )

    raw_itinerary = response.choices[0].message.content
    formatted_itinerary = format_itinerary(raw_itinerary)

    return render_template('confirmation.html', itinerary=formatted_itinerary)

def format_itinerary(text):
    # Regular expression to find patterns and bold them
    bold_pattern = re.compile(r"\*\*(.+?)\*\*")
    # Replace **Text** with HTML <strong>Text</strong>
    text = bold_pattern.sub(r"<strong>\1</strong>", text)

    # Split the text at two new lines assuming each block separated by two new lines is a day
    days = text.split('\n\n')
    formatted_text = []

    # Wrap each block in a div with a class for styling
    for day in days:
        if day.strip():  # Ensure the block isn't just empty space
            formatted_text.append(f'<div class="day">{day.strip()}</div>')

    return ''.join(formatted_text)

if __name__ == '__main__':
    app.run(debug=True)