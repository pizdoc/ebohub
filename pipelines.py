from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self):
        self.db = MongoClient().ebohub
        # create indexes or pohui

    def process_item(self, item, spider):
        try:
            self.db.videos.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)
        except Exception as e:
            self.logger.error(e)
        return item