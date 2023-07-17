
# from crypt import methods
import requests as req
import cv2
import urllib.request
import numpy as np
import base64
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS

app = Flask(__name__)


def get_image(imagepath):
    url = "https://ilocr.iiit.ac.in/layout/"
    payload = {"model": "dbnet"}
    files = [("images", (imagepath, open(imagepath, "rb"), "image/jpeg"))]
    headers = {}

    response = req.post(url, headers=headers, data=payload, files=files)

    print(response.json()[0]["regions"])
    regions = response.json()[0]["regions"]
    image = cv2.imread(imagepath)

    for i in response.json()[0]["regions"]:
        print(i["bounding_box"])
        tlx = int(i["bounding_box"]["x"]) - int(i["bounding_box"]["w"]) // 2
        tly = int(i["bounding_box"]["y"]) - int(i["bounding_box"]["h"]) // 2
        brx = int(i["bounding_box"]["x"]) + int(i["bounding_box"]["w"]) // 2
        bry = int(i["bounding_box"]["y"]) + int(i["bounding_box"]["h"]) // 2
        cv2.rectangle(
            img=image,
            rec=(
                int(i["bounding_box"]["x"]),
                int(i["bounding_box"]["y"]),
                int(i["bounding_box"]["w"]),
                int(i["bounding_box"]["h"]),
            ),
            color=(0, 0, 255),
            thickness=2,
        )

    return image

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/process-image', methods=['POST'])
def process_image():
    # Retrieve the image data from the request
    image_data = request.json.get("image_data")

    # Decode the base64 image data and convert it to a NumPy array
    _, encoded_data = image_data.split(",", 1)
    decoded_data = base64.b64decode(encoded_data)
    nparr = np.frombuffer(decoded_data, np.uint8)

    # Read the image using OpenCV
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform any processing on the image
    # ...
    cv2.imwrite("output.jpeg",img)

    # Return the processed image as base64 encoded string
    processedimg = get_image("output.jpeg")
    _, encoded_image = cv2.imencode('.jpg', processedimg)
    image_data = base64.b64encode(encoded_image).decode('utf-8')
    
    return render_template("resultpage.html",img_data =  image_data)


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code
    result = data['value'] * 2
    return jsonify(result=result) # return the result to JavaScript

@app.route('/testpage', methods=['GET'])
def testPage():
    return {"data":"successfully connected"}
  
if __name__ == '__main__':
    # app.run(debug=False,port=5001)
    app.run(debug=False,host='0.0.0.0',port=5001)