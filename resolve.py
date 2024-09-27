import csv
from datetime import datetime


# 读取原始数据并拆解日期
def split_date(csv_input, csv_output):
    # 打开输入的CSV文件
    with open(csv_input, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # 创建新的字段名，不包括release_date
        fieldnames = ['title', 'release_year', 'release_month', 'release_day', 'description', 'score']

        # 打开输出的CSV文件
        with open(csv_output, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            # 写入表头
            writer.writeheader()

            # 遍历每一行数据
            for row in reader:
                # 拆解日期
                try:
                    # 将"Month Day, Year"转换为datetime对象
                    release_date = datetime.strptime(row['release_date'], '%b %d, %Y')

                    # 拆解为年、月、日
                    release_year = release_date.year
                    release_month = release_date.month
                    release_day = release_date.day

                    # 将修改后的数据写入新的CSV文件，不包括release_date
                    writer.writerow({
                        'title': row['title'],
                        'release_year': release_year,
                        'release_month': release_month,
                        'release_day': release_day,
                        'description': row['description'],
                        'score': row['score']
                    })
                except ValueError:
                    print(f"Skipping invalid date format: {row['release_date']}")


# 运行函数，指定输入和输出的CSV文件名
split_date('Movie_Untreated.csv', 'Movie.csv')

print("Date fields have been split and saved to Movie_with_split_date.csv")
