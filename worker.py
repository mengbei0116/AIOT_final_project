# worker.py
import os
import sys
from rembg import remove
from PIL import Image

def process_folder(filedir):
    input_folder = os.path.join('images', filedir, 'default')
    output_folder = os.path.join('output_images', filedir)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')
            try:
                with Image.open(input_path) as img:
                    output = remove(img)
                    output.save(output_path)
                    print(f'{filedir}: 完成 → {filename}')
            except Exception as e:
                print(f'{filedir}: 錯誤處理 {filename} → {e}')

if __name__ == '__main__':
    folder_name = sys.argv[1]  # 由主程式傳入資料夾名稱
    process_folder(folder_name)
