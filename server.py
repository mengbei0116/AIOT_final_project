from flask import Flask, jsonify, render_template, request
import cv2
import datetime
import os
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import random
from torchvision.transforms.functional import to_pil_image
from collections import defaultdict

# 初始化
app = Flask(__name__)
category_counts = defaultdict(int)
history_log = defaultdict(list)

class_names = ['aluminum_soda_cans', 'cardboard_boxes', 'plastic_water_bottles', 'paper_cups']
class_mapping = {
    0: "鐵鋁罐",
    1: "紙餐盒",
    2: "寶特瓶",
    3: "紙杯"
}

# 反標準化
unnormalize = transforms.Normalize(
    mean=[-m/s for m, s in zip([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])],
    std=[1/s for s in [0.229, 0.224, 0.225]]
)

def save_tensor_as_image(tensor, filename):
    img = unnormalize(tensor.squeeze(0)).clamp(0, 1)  
    img_pil = to_pil_image(img)
    os.makedirs('rotated_image', exist_ok=True)
    img_pil.save(os.path.join('rotated_image', filename))

@app.route('/capture', methods=['GET'])
def capture_image():
    cap = cv2.VideoCapture(0) 
    ret, frame = cap.read()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'photo_{timestamp}.jpg'
        test_image_dir = 'captured_images/'
        os.makedirs(test_image_dir, exist_ok=True)
        image_path = os.path.join(test_image_dir, filename)
        cv2.imwrite(image_path, frame)

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        testmodel = torch.load('waste_classification_model_resnet.pth')
        testmodel.eval().to(device)

        image = Image.open(image_path).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(device)
        save_tensor_as_image(input_tensor, filename)
        
        with torch.no_grad():
            output = testmodel(input_tensor)
            probabilities = F.softmax(output, dim=1)
            predicted_idx = output.argmax(1).item()
            predicted_class = class_names[predicted_idx]

        # 類別對應
        if predicted_class.startswith('aluminum_') or predicted_class.startswith('steel'):
            class_num = 0
        elif predicted_class.startswith('paper_meal'):
            class_num = 1
        elif predicted_class.startswith('plastic'):
            class_num = 2
        elif predicted_class.startswith('paper_c'):
            class_num = 3
        else:
            class_num = -1  # 意外類別

        if class_num >= 0:
            category_counts[class_num] += 1
            history_log[class_num].append(category_counts[class_num])

        return f"{class_num}", 200
    else:
        return "Failed to capture", 500

@app.route('/status')
def get_status():
    return jsonify({
        "counts": dict(category_counts),
        "history": dict(history_log)
    })

@app.route('/reset/<int:class_id>', methods=['POST']) 
def reset_class_count(class_id):
    if class_id in category_counts:
        category_counts[class_id] = 0
        history_log[class_id] = []
        return jsonify({"message": f"Class {class_mapping[class_id]} reset successfully."}), 200
    else:
        return jsonify({"error": "Invalid class ID."}), 400

@app.route('/')
def dashboard():
    return render_template("web.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
