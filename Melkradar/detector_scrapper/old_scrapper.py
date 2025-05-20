import json
import time
import pika
import requests


class Data:
    def __init__(self, url, estate, count, page_num):
        self.url = url
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "application/json;q=0.9, */*;q=0.1",
            "Accept-Language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "Content-Type": "application/json; charset=utf-8; odata.metadata=minimal"
        }
        self.payload = {
            "SearchInfo": {
                "EstateTypeGroup": f"{estate}",
                "EstateTypeList": [],
                "AdvertTypeGroup": None,
                "AdvertTypeList": [],
                "CityAreaGroups": [],
                "City_Id": None,
                "AreaSizeFrom": None,
                "AreaSizeTo": None,
                "SellTotalPriceMin": None,
                "SellTotalPriceMax": None,
                "RentMortgagePriceMin": None,
                "RentMortgagePriceMax": None,
                "RentMonthlyPriceMin": None,
                "RentMonthlyPriceMax": None,
                "Bedrooms": [],
                "IsFullMortgage": False,
                "BuildingAgeMax": None,
                "BuildingAgeMin": None
            },
            "PageNo": page_num,
            "PageSize": count
        }

    def get_data(self):
        try:
            return requests.post(self.url, headers=self.header, json=self.payload).json()["value"]
        except Exception as e:
            print("there was an error", e)


class MelkRadarAd:
    def __init__(self, data_json):
        self.id = data_json["EasyKey"]
        self.url = data_json["Url"]
        self.name = data_json["Summary"].split('\n')[0].split('-')[0]
        self.address = data_json['VendorCityAreaTitle']
        self.price = data_json["SellTotalPrice"] if data_json[
                                                        "AdvertType"] == "Sale" else f'{data_json["RentMortgagePrice"]} ,{data_json["RentMonthlyPrice"]}'
        self.area = data_json["AreaSize"]
        self.room_count = data_json["BedroomCount"]
        self.year = data_json["BuiltDateStr"]
        self.feats = None
        self.images = data_json["VendorImageUrls"].split(',') if data_json["VendorImageUrls"] else None

    def get_final_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name,
            "address": self.address,
            "price": self.price,
            "area": self.area,
            "room_count": self.room_count,
            "year": self.year if self.year else None,
            "feats": self.feats,
            "images": self.images
        }


def rabbit_publish(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='scrapper_queue__MelkRadar')
    channel.basic_publish(
        exchange='',
        routing_key='scrapper_queue__MelkRadar',
        body=json.dumps(data)
    )
    connection.close()


def get_new_data():
    try:
        url = "https://melkradar.com/p/odata/PeoplePanel/estateMarker/getAdvers"
        final_data_list = []
        # Getting 4000 Listings
        for page_num in range(1, 11):
            apartment_data = Data(url, "Apartment", 200, page_num)
            office_data = Data(url, "Office", 200, page_num)
            for apartment in apartment_data.get_data():
                apartment_json = MelkRadarAd(apartment).get_final_json()
                final_data_list.append(json.dumps(apartment_json, indent=4))
            for office in office_data.get_data():
                office_json = MelkRadarAd(office).get_final_json()
                final_data_list.append(json.dumps(office_json, indent=4))
        print(len(final_data_list))
        rabbit_publish(final_data_list)
    except Exception as e:
        print("an Error occurred", e)
        time.sleep(10)


if __name__ == '__main__':
    get_new_data()
