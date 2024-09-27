import requests
from bs4 import BeautifulSoup
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 爬取的基础URL和参数
base_url = "https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2024&page="


# 定义一个函数用于爬取单个页面
def scrape_page(page):
    url = base_url + str(page)
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # 检查请求是否成功
    except requests.HTTPError as e:
        print(f"Error fetching page {page}: {e}")
        return []  # 返回空列表表示该页没有数据

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_cards = soup.find_all(class_="c-finderProductCard")

    movies = []

    # 提取每个电影的详细信息
    for card in movie_cards:
        try:
            title = card.find(class_="c-finderProductCard_titleHeading").find_all("span")[1].get_text(strip=True)
            release_date = card.find(class_="c-finderProductCard_meta").find(class_="u-text-uppercase").get_text(
                strip=True)
            description = card.find(class_="c-finderProductCard_description").get_text(strip=True)
            score = card.find(class_="c-siteReviewScore").find("span").get_text(strip=True)
            movies.append({
                'title': title,
                'release_date': release_date,
                'description': description,
                'score': score
            })
        except AttributeError:
            print(f"Skipping a movie on page {page} due to missing information.")
            continue  # 跳过数据不完整的电影

    print(f"Completed page {page}")
    return movies


# 打开CSV文件，准备写入数据
with open('Movie_Untreated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # 定义字段名（表头）
    fieldnames = ['title', 'release_date', 'description', 'score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 使用多线程抓取页面
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有任务
        futures = {executor.submit(scrape_page, page): page for page in range(1, 501)}

        # 处理完成的任务
        for future in as_completed(futures):
            page = futures[future]
            try:
                movies = future.result()
                # 写入电影信息到CSV文件
                for movie in movies:
                    writer.writerow(movie)
            except Exception as e:
                print(f"Error processing page {page}: {e}")

print("All data has been saved to Movie.csv")
