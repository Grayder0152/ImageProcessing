import datetime

from flask import render_template, request, json

from main import app
from main.services import generate_part_images, clean_images_folder, get_or_create_client, create_task


@app.route('/')
def index():
    clean_images_folder()
    return render_template('index.html')


@app.route('/get_img', methods=['POST'])
def get_img():
    if 'img' in request.files:
        img = request.files['img']

        start_proc_time = datetime.datetime.now()
        images_name = generate_part_images(img)
        stop_proc_time = datetime.datetime.now()

        client = get_or_create_client(request)

        create_task(
            filename=img.filename,
            start_proc_time=start_proc_time,
            stop_proc_time=stop_proc_time,
            client_id=client.id
        )

        return json.dumps({'status': 'OK', 'images_name': images_name})
    return json.dumps({'status': 'Error'})
