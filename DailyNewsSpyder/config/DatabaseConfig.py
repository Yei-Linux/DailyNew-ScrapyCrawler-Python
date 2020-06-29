from pymongo import MongoClient

class DatabaseConfig():
    def __init__(self):
        self.db = MongoClient(
            "mongodb+srv://root:123@cluster0-sqpjf.mongodb.net/daily-news?retryWrites=true&w=majority"
        )['daily-news']

    def getCollection(self,collectionName):
        return self.db[collectionName]

    def resetCollection(self,collectionName):
        self.db[collectionName].drop()


