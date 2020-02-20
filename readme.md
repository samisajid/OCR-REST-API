# POST /image-sync

Accept the image as a b64-encoded payload data:

curl -XPOST "http://localhost:5000/image-sync" -d '{"image_data": "<b64 encoded image>"}'
  
It should return a response, content-type application/json:

{
"text": "<recognized text>"
}

# POST /image and GET /image

The POST /image-sync API is actually not so good, because OCR may take
some time, especially for large images. It is generally bad practices to have
http services which takes multiple seconds or worse to respond. We thus ask to
add another API that works as follows. The input is exactly the same as for
/image-sync:

curl -XPOST "http://localhost:5000/image" 
-d '{"image_data": "<b64 encoded image>"}'

But instead, it should return a response, content-type application/json:

{
"task_id": "<task id>"
}

The task id can then be used to retrieve the OCR text with the GET /image:

curl -XGET "http://localhost:5000/image" -d '{"task_id": "<task id as received from POST /image>"}'

and return a response, content-type application/json:

{
"task_id": "<recognized text>"
}

if the task is done, or:

{
"task_id": null,
}

In which case it is assumed the task is not finished yet.

# How to run the API?

Build the docker image using this command:

$ docker build <path_to_docker_file> -t <some_tag>

Then run a container using this command

$ docker run -p 5000:5000 <image_tag_or_id>

Once you run the container, you can start using the API. To get the text from an image, convert it first to base64 string (you can use https://www.browserling.com/tools/file-to-base64 ). then use it to post an image with the following command:

$ curl -H "Content-Type: application/json" -d '{"image_data": "<b64 encoded image>"}' -X POST http://localhost:5000/image

Use the task id returned by POST to get the recognized text of the image using this command:

$ curl -H "Content-Type: application/json" -d '{"task_id":"<task id as received from POST /image>"}'-X GET http://localhost:5000/image

You can get all the tasks and the recognized texts done so far using the following command:

$ curl -X GET http://localhost:5000/allimages
