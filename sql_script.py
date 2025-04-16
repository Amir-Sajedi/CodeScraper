import pika
import json
import time
import pymysql


def rabbit_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='scrapper_queue__MelkRadar')
    while True:
        # method_frame: metadata about the message (e.g., delivery tag, etc.) (is None if there aren't any messages received)
        #
        # header_frame: headers and properties (Not needed here)
        #
        # body: the actual message you sent from the detector
        method_frame, header_frame, body = channel.basic_get(queue='scrapper_queue__MelkRadar', auto_ack=True)
        if (method_frame):
            data = json.loads(body)
            database_publish(data)
            time.sleep(10)
        else:
            time.sleep(10)


def database_publish(data):
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='codescrapper',
        charset='utf8mb4'
    )
    cursor = db.cursor()
    for listing in data:
        listing = json.loads(listing)
        sql = """
         INSERT INTO listings (id, url, name, address, price, area, room_count, year, feats, images)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         """
        feats_json = json.dumps(listing['feats'], ensure_ascii=False)
        images_json = json.dumps(listing['images'], ensure_ascii=False)
        values = (
            listing['id'],
            listing['url'],
            listing['name'],
            listing['address'],
            f'{int(listing["price"]):,}' if str(listing['price']).isnumeric() else listing['price'],
            listing['area'],
            listing['room_count'],
            int(listing['year']) if listing['year'] else None,
            feats_json,
            images_json
        )
        try:
            cursor.execute(sql, values)
        except Exception as e:
            print("Error", e)
    db.commit()
    cursor.close()
    db.close()
    print("Data got transfered!")


if __name__ == '__main__':
    rabbit_consume()
