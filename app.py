
# from crypt import methods
import requests as req
import cv2
import urllib.request
import numpy as np
import pygame
import base64
from flask import Flask,request,jsonify,render_template
from flask_cors import CORS

app = Flask(__name__)

def setup_screen_sprite(impath):
    img = pygame.image.load(impath)
    rect = img.get_rect()

    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    screen = pygame.display.set_mode((rect.w, rect.h))

    sprite = pygame.sprite.Sprite()
    sprite.image = img
    sprite.rect = rect
    return screen, sprite, surf

def render_text_on_images(imgpath,wordparams):
        pygame.init()
        fontpath = r"D:\web projects\new_api_test\EkMukta-Regular.ttf"
        screen, sprite, surf = setup_screen_sprite(imgpath)
        mf = pygame.font.Font(fontpath,size=15)
        mf.set_script("Deva")
        mf.set_bold(1)
        sequence = []
        for i in wordparams:
            word = i[0]
            
            point = [i[1],i[2]]
            ren = mf.render(word, False, (0, 255, 0))
            sequence.append((ren, (point[0], point[1] - mf.get_height() + 7.5)))
            surf.blits(sequence)
            sprite.image.blit(surf, sprite.rect)
        grp = pygame.sprite.Group()
        grp.add(sprite)
        grp.draw(screen)
        pygame.display.flip()
        pygame.image.save_extended(screen, "output.jpeg")
        return 1
        

def get_image(imagepath):
    wordparams = []
    url = "http://172.31.46.187:8889/recognize/"
    payload = {"model": "dbnet_parseq"}
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
            thickness=1,
        )
        label = i['label']
        wordparams.append([label,i["bounding_box"]["x"],i["bounding_box"]["y"]])
    cv2.imwrite("processedinput.jpeg",image)
    render_text_on_images("processedinput.jpeg",wordparams)
    




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/process-image', methods=['POST','GET'])
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
    cv2.imwrite("input.jpeg",img)

    # Return the processed image as base64 encoded string
    hello = get_image("input.jpeg")
    outputimg = cv2.imread("output.jpeg")
    _, encoded_image = cv2.imencode('.jpg', outputimg)
    
   
    output_image_data = base64.b64encode(encoded_image).decode('utf-8')
    processedinputimg = cv2.imread("processedinput.jpeg")
    _, encoded_input_image = cv2.imencode('.jpg', processedinputimg)
    input_image_data = base64.b64encode(encoded_input_image).decode('utf-8')
    
    return render_template("resultpage.html",output_img_data =  output_image_data,input_img_data = input_image_data)


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