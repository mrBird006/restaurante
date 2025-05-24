from typing import List, Dict, Optional
from pymongo import MongoClient
from .client import PlateDataClient


class MongoPlateDataClient(PlateDataClient):
    def __init__(self, connection_string: str, db_name: str = "menu", collection_name: str = "plates"):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_plates(self) -> List[Dict]:
        return list(self.collection.find({}, {'_id': False}))

    def get_plate_by_slug(self, slug: str) -> Optional[Dict]:
        return self.collection.find_one({'slug': slug}, {'_id': False})

    def add_like(self, slug: str, email: str) -> None:
        self.collection.update_one(
            {'slug': slug},
            {
                '$addToSet': {'likes': email},
                '$pull': {'dislikes': email}
            }
        )

    def add_dislike(self, slug: str, email: str) -> None:
        self.collection.update_one(
            {'slug': slug},
            {
                '$addToSet': {'dislikes': email},
                '$pull': {'likes': email}
            }
        )

    def remove_reaction(self, slug: str, email: str) -> None:
        self.collection.update_one(
            {'slug': slug},
            {
                '$pull': {
                    'likes': email,
                    'dislikes': email
                }
            }
        )

    def add_comment(self, slug: str, name: str, comment: str) -> None:
        self.collection.update_one(
            {'slug': slug},
            {
                '$push': {
                    'comments': {'name': name, 'text': comment}
                }
            }
        )
