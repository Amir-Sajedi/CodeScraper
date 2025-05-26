import pika
import json
import time
import requests
import re
from bs4 import BeautifulSoup as bs
import jdatetime

shamsi_date = jdatetime.date.today()


class house:
    def __init__(self, url):
        self.url = url

    def get_data(self):

        response = requests.get(self.url)
        if response.status_code == 200:
            self.html = bs(response.content, 'html.parser')
        else:
            print(f"Failed to retrieve data from {self.url}")
            self.html = None

    def parse_html(self):
        if self.html:
            data = {}
            data["url"] = self.url
            data["id"] = self.html.find("div", {"class": "col-md-4 col-sm-4 col-lg-4 col-xs-12 col-12"}).text
            data["id"] = re.findall(r'\d+', data["id"])[0]

            data["price"] = self.html.find("div", {"class": "col-md-2 col-sm-2 col-lg-5 card-body ForPrint"}).text
            data["price"] = data["price"].replace(',', '')
            data["price"] = re.findall(r'\d+', data["price"])
            data["type"] = self.html.find("div", {"class": "col-md-4 col-sm-4 col-lg-3 col-xs-12 col-12"}).text
            if "فروش" in data["type"]:
                data["type"] = "فروش"
                data["address"] = self.html.find("div", {"class": "col-md-4 col-sm-4 col-lg-5 adds"}).text
                data["price"] = data["price"][0]
            else:
                data["type"] = "اجاره"
                data["address"] = self.html.find("div", {"class": "col-md-4 col-sm-4 col-lg-4 adds"}).text
                data["price"] = data["price"][0] + ',' + data["price"][1]

            options = self.html.find_all('div', {"class": "col-md-4 col-sm-4 col-lg-4 col-xs-12"})
            options_text = ""

            for option in options:
                options_text += option.text + "\n"

            data["area"] = re.search(r'زیربنا\s*:?\s*(\d+)', options_text).group(1)
            data["room_count"] = re.search(r'تعداد خواب\s*:?\s*(\d+)', options_text).group(1)
            data["year"] = re.search(r'سن بنا\s*:?\s*(\d+)', options_text).group(1)
            data["year"] = str(shamsi_date.year - int(data["year"]))
            data["images"] = []
            data["feats"] = None
            data["name"] = data["address"]
            image_number = 1
            while True:
                try:
                    response = requests.get(
                        "https://maskan-file.ir/img/FilesImages/{}_{}.jpg".format(data["id"], image_number))
                    if "notfound" in response.text:
                        break
                    data["images"].append(
                        "https://maskan-file.ir/img/FilesImages/{}_{}.jpg".format(data["id"], image_number))
                    image_number += 1
                except:
                    break
            return json.dumps(data)


def rabbit_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='detector_queue')
    while True:
        # method_frame: metadata about the message (e.g., delivery tag, etc.) (is None if there aren't any messages received)
        #
        # header_frame: headers and properties (Not needed here)
        #
        # body: the actual message you sent from the detector
        method_frame, header_frame, body = channel.basic_get(queue='detector_queue', auto_ack=True)
        if (method_frame):
            data = json.loads(body)
            process(data)
        else:
            time.sleep(2)


def rabbit_publish(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='scrapper_queue__MaskanFile')
    channel.basic_publish(
        exchange='',
        routing_key='scrapper_queue__MaskanFile',
        body=json.dumps(data)
    )
    connection.close()


def process(data):
    responses = []
    for dt in data:
        ad = house(dt)
        ad.get_data()
        try:
            responses.append(ad.parse_html())
        except Exception as e:
            print("Error", e)
    rabbit_publish(responses)


if __name__ == '__main__':
    rabbit_consume()
