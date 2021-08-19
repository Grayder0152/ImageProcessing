import os
import hashlib
from PIL import Image
from io import BytesIO

from main import db
from main.models import Client, Task


def generate_part_images(img):
    images_name = []
    img_data = img.read()
    main_img_name = img.filename.split(".")

    im = Image.open(BytesIO(img_data))
    img_width, img_height = im.size

    for i in range(5):
        part_img_name = f'{main_img_name[0]}_{i}.{main_img_name[-1]}'

        left = img_width * (0.2 * i)
        right = img_width * (0.2 * (i + 1))
        top = img_height * abs((1 / 3) - (1 / 3) * (0.5 * i))
        bottom = img_height * (1 - abs((1 / 3) - (1 / 3) * (0.5 * i)))

        part_img = im.crop((left, top, right, bottom))
        part_img.save(f'main/static/images/{part_img_name}', quality=95)

        images_name.append(part_img_name)
    return images_name


def clean_images_folder():
    folder = '/static/images/'
    path = os.path.abspath(os.path.dirname(__file__)) + folder
    images = os.listdir(path)
    if len(images) > 25:
        for img in images:
            os.remove(path + img)


def get_or_create_client(request):
    client_ip = request.remote_addr
    hash_client_ip = hashlib.sha256(client_ip.encode('utf-8')).hexdigest()

    client = Client.query.filter_by(ip=hash_client_ip).first()
    if client is None:
        client = Client(ip=hash_client_ip)
        db.session.add(client)
        db.session.commit()
    return client


def create_task(filename, start_proc_time, stop_proc_time, client_id):
    task = Task(file_name=filename, start_proc_at=start_proc_time, stop_proc_at=stop_proc_time, client_id=client_id)
    db.session.add(task)
    db.session.commit()
