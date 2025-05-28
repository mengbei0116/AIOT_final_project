# main.py
import os
import subprocess

input_root = 'images'

if __name__ == '__main__':
    subfolders = [d for d in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, d))]
    
    processes = []
    for folder in subfolders:
        # 開啟一個 subprocess 執行 worker.py
        p = subprocess.Popen(['python', 'worker.py', folder])
        processes.append(p)

    # 等待所有子程式結束
    for p in processes:
        p.wait()
