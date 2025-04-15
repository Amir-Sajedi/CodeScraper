import json
import pymysql

with open('E:/Sql_data/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

db = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',  
    database='scraped_data',
    charset='utf8mb4'  
)

cursor = db.cursor()

for row in data:
    sql = """
    INSERT INTO properties (id, url, name, address, price, area, room_count, year, feats, images)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    feats_json = json.dumps(row['feats'], ensure_ascii=False)
    images_json = json.dumps(row['images'], ensure_ascii=False)
    values = (
        row['id'],
        row['url'],
        row['name'],
        row['address'],
        row['price'],
        int(row['area']),
        int(row['room_count']),
        int(row['year']),
        feats_json,
        images_json
    )
    cursor.execute(sql, values)

db.commit()
cursor.close()
db.close()
print("Data got transfered!")