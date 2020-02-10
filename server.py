#!flask/bin/python
from flask import Flask, jsonify, request
import threading
import tesserocr
import base64
import os
import uuid
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True



app = Flask(__name__)

# Data to serve with our API
images = {0:{"task_id":0,"recognized_text": "Hello world!"}}

static_id=0

@app.route('/allimages', methods=['GET'])
def get_tasks():
    """
    This fuction returns all the images proceded with their id and the texts they contain
    Usage: curl -X GET http://localhost:5000/allimages
    """
    return jsonify({'images': images})

@app.route('/image', methods=['GET'])
def get_task():
    """
    This fuction returns the text in the image corresponding to the task id received from POST /image>
    Usage: curl -H "Content-Type: application/json" -d '{"task_id":"<task id as received from POST /image>"}'-X GET http://localhost:5000/image
    """
    if not request.json or not 'task_id' in request.json:
        return 'Expected JSON format: {"task_id":"<task id as received from POST /image>"}\n',400
    task=int(request.json['task_id'])
    try:
        return jsonify({task:images[task]["recognized_text"]})
    except:
        return "The task_id {} is not in the base".format(request.json['task_id'])

@app.route('/image', methods=['POST'])
def create_task():
    """
    This function launch a thread for OCR processing of a base64 encoded image
    Usage: curl -H "Content-Type: application/json" -d '{"image_data": "<b64 encoded image>"}' -X POST http://localhost:5000/image
    """
    if not request.json or not 'image_data' in request.json:
        return 'Expected JSON format: {"image_data":"<b64 encoded image>"}\n',400
    global static_id
    static_id+=1
    img = {static_id:
        {
            'task_id': static_id,
            'recognized_text': None
        }
    }
    images.update(img)
    x = threading.Thread(target=ocr,args=(request.json["image_data"],static_id))
    x.start()
    return jsonify({"task_id":static_id}), 201
def ocr(b64, task_id):
    """
    This function process the base64 image and returns any text contained int the image
    """
    task=str(task_id)
    with open(task, "wb") as image_file:
        try:
            image_file.write(base64.b64decode(b64))
        except:
            os.system("rm {}".format(task))            
            return ('Unable to decode the base64 string')
    img=Image.open("{}".format(task))
    text=tesserocr.image_to_text(img)
    images[task_id]={"task_id":task_id,"recognized_text": text.replace('\n','      ')}
    os.system("rm {}".format(task))
    return

if __name__ == '__main__':
    
    app.run(debug=True,host='0.0.0.0')