from logging import Logger

from custom_components.silesiaalert.http_client import HttpClientInterface

from marshmallow import Schema, fields, post_load

from dataclasses import dataclass
from typing import List


@dataclass
class AlertData:
    id: str
    name: str
    tag: str
    lat: float
    lon: float
    createdAt: str
    lastUpdate: str
    currentStatus: int
    isPrivate: bool

    @classmethod
    def from_json(cls, json_data: str) -> "AlertData":
        alert_data_collection: AlertData = AlertDataSchema().loads(json_data=json_data, many=True)
        return alert_data_collection


class AlertDataSchema(Schema, many=True):
    id = fields.Str()
    name = fields.Str()
    tag = fields.Str()
    lat = fields.Float()
    lon = fields.Float()
    createdAt = fields.Str()
    lastUpdate = fields.Str()
    currentStatus = fields.Int()
    isPrivate = fields.Bool()

    @post_load
    def make_alert_data(self, data, **kwargs):
        return AlertData(**data)


class SilesiaAlertApi:

    def __init__(self, http_client: HttpClientInterface, logger: Logger) -> None:
        self.__http_client: HttpClientInterface = http_client
        self.__logger: Logger = logger

    async def fetch_data(self):
        # sample data from https://silesiaalert.pl/dane5.json
        # [
        #     {
        #         "id": "02c802e5-938d-4c6b-a108-85268936e30c",
        #         "name": "Mikołów",
        #         "tag": "45",
        #         "lat": 50.168,
        #         "lon": 18.9032,
        #         "createdAt": "2023-08-07T11:43:35.721057",
        #         "lastUpdate": "2024-07-21T05:25:07.093013",
        #         "currentStatus": 0,
        #         "isPrivate": false
        #     },
        #     {
        #         "id": "0584d971-b3b9-43f1-8621-0286bcbbe544",
        #         "name": "Kłobuck",
        #         "tag": "33",
        #         "lat": 50.9045,
        #         "lon": 18.9367,
        #         "createdAt": "2023-05-22T11:53:30.623162",
        #         "lastUpdate": "2024-07-21T05:25:07.093013",
        #         "currentStatus": 0,
        #         "isPrivate": false
        #     },
        #     {
        #         "id": "082e621a-ccb1-4f3e-b86c-a936d0e8d4bf",
        #         "name": "Lubliniec",
        #         "tag": "32",
        #         "lat": 50.6679,
        #         "lon": 18.6859,
        #         "createdAt": "2023-05-22T11:52:48.043427",
        #         "lastUpdate": "2024-07-21T05:25:07.093014",
        #         "currentStatus": 0,
        #         "isPrivate": false
        #     }
        # ]

        json = await self.__http_client.make_request('https://silesiaalert.pl/dane5.json')

        return AlertData.from_json(json)

