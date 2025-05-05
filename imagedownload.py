from icrawler.builtin import GoogleImageCrawler

# categories = {
#     'paper_cup': '手搖飲 紙杯',
#     'plastic_bottle': 'plastic bottle isolated white background',
#     'aluminum_can': 'aluminum can isolated white background',
#     'cardboard_box': 'cardboard box isolated white background',
# }

categories = {
    'paper_cup': 'disposable cup OR beverage cup',
}

for folder, keyword in categories.items():
    crawler = GoogleImageCrawler(storage={'root_dir': f'dataset/{folder}'})
    crawler.crawl(keyword=keyword, max_num=500, file_idx_offset=0)
