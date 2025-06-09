from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import os

categories = {
    'tetra pak': '鋁箔包',
}
os.makedirs('dataset', exist_ok=True)
# categories = {
#     'aluminum_can': 'aluminum can isolated white background'
# }

for folder, keyword in categories.items():
    folder_path = f'dataset/{folder}'
    os.makedirs(folder_path, exist_ok=True)  # 如果資料夾不存在，則建立
    crawler = BingImageCrawler(storage={'root_dir': folder_path})
    crawler.crawl(keyword=keyword, max_num=500, file_idx_offset=0)