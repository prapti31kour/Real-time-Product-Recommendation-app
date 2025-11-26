import base64,json
import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from ultralytics import YOLO
import cv2
from predict_img import *
from recommend_img import *

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# app = Flask(__name__, static_url_path='static')
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "xshgfdyhjsfyujc"

@app.route('/')
def home():
    return render_template("home_page.html")

@app.route("/redirect_second")
def redirect_second():
    return render_template("second_page.html")

@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        data = request.json
        if 'image' not in data:
            return jsonify(status='error', message='No image data found'), 400
        
        dataURL = data['image']
        app.logger.debug("Received data: %s", dataURL)  # Log the first 30 characters for debugging

        # Extract base64 part of the data URL
        base64_str = dataURL.split(',')[1]
        
        # Decode the Base64 string
        image_data = base64.b64decode(base64_str)
        
        # Save the image to a file
        img_dir = os.path.join('.', 'static/images')
        # img_dir = 'C:/Users/User/Downloads/HackOn/website/static/images'
        img_path = os.path.join(img_dir, 'snap.jpg')
        
        # cv2.imwrite(img_path, image_data)
        with open(img_path, "wb") as f:
            f.write(image_data)
        
        # predict function
        predict()
        
        return jsonify(status='success', message='Image uploaded successfully')
    except Exception as e:
        app.logger.error("Error: %s", e)  # Log the error
        return jsonify(status='error', message=str(e)), 400
    
    
@app.route('/img_recommend',  methods=['POST'])
def img_recommend():
    try:
        # Requesting data from html file
        data = request.form['data']
        app.logger.debug(f"Received data: {data}")
        
        # Path to the JSON file
        json_file_path = os.path.join('.', 'static/detected_obj.json')
        
        # Load JSON file from the file
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)

        # Function to get values by key
        def get_values_by_key(input_key, json_data):
            if input_key in json_data:
                return json_data[input_key]
            else:
                return None
        
        # Fetching the values from JSON file
        values = get_values_by_key(data, json_data)

        if values:
            for item in values:
                for detected_object_class, photo_name in item.items():
                    recommend(detected_object_class, photo_name)
                    app.logger.debug(f"Key: {detected_object_class}, Value: {photo_name}")
        else:
            app.logger.debug(f"Key '{data}' not found in the json file.")
        
        print("10101010chgvcjhbchj")
        # render_template('cond_page.html')
        return jsonify(status='Successful')
        # return render_template("third.html")
    except Exception as e:
        app.logger.error(f"Error in img_recommend: {e}")
        return jsonify(status='error', message=str(e)), 400
    # return jsonify(status='success', message='Recommendations uploaded successfully')
        

if __name__ == '__main__':
    app.run(debug=True)

