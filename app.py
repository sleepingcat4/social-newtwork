from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import csv
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

# Set the path to your image folder
image_folder = r"F:\Dataset\face"
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
current_image_index = 0

# CSV file to record ratings
csv_file = "ratings.csv"

# Target size for resizing
target_size = (500, 500)

# List to store original image names
original_image_names = []

@app.route('/')
def index():
    global current_image_index
    if current_image_index >= len(image_files):
        return "Thanks for Rating!"

    current_image_name = image_files[current_image_index]
    current_image_path = os.path.join(image_folder, current_image_name)
    image_data = get_resized_image_data(current_image_path, target_size)

    # Store the original image name
    original_image_names.append(current_image_name)

    return render_template('index.html', image=image_data)

@app.route('/rate', methods=['POST'])
def rate():
    global current_image_index
    image_id = original_image_names[current_image_index]
    rating = request.form['rating']

    with open(csv_file, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([image_id, rating])

    current_image_index += 1

    if current_image_index >= len(image_files):
        return redirect(url_for('rate_page'))

    return redirect(url_for('index'))

@app.route('/rate_page')
def rate_page():
    return render_template('rate.html')

@app.route('/download-ratings')
def download_ratings():
    # Create a response with the CSV file
    return send_file(csv_file, as_attachment=True, download_name='ratings.csv')

def get_resized_image_data(image_path, size):
    img = Image.open(image_path)
    img = img.resize(size)

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/jpeg;base64,{img_str}"

if __name__ == '__main__':
    app.run(debug=False)
