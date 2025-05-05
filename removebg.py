import os
from rembg import remove
from PIL import Image

input_folder = 'dataset'
output_folder = 'output_images'

os.makedirs(output_folder, exist_ok=True)

for filedir in os.listdir(input_folder):
    for filename in os.listdir(os.path.join(input_folder, filedir)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filedir, filename)
            output_path = os.path.join(output_folder, filedir, os.path.splitext(filename)[0] + '.png')

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path)
                print(f'完成：{filename} → {output_path}')

