import json
import datetime

from DailyNewsSpyder.config.DatabaseConfig import DatabaseConfig
from DailyNewsSpyder.helpers.CleanDataHelper import CleanDataHelper

class ScrapingSiteHelper():
    @staticmethod
    def parseDataBySite(response):
        listArticles = []
        site = response.meta.get('site')

        for article in response.css(site['components']['article']):
            header = article.css(site['components']['header']).get()
            description = article.css(site['components']['description']).get()
            newUrl = ScrapingSiteHelper.format_url(article.css(site['components']['newUrl']).get(), site['baseUrl'])
            imageUrl = article.css(site['components']['imageUrl']).get()

            if header is not None and description is not None and newUrl is not None and imageUrl is not None:
                dataJson = dict(
                    title= CleanDataHelper.deleteMultipleWhiteSpaces(header),
                    description= CleanDataHelper.deleteMultipleWhiteSpaces(description),
                    urlImage= CleanDataHelper.deleteMultipleWhiteSpaces(imageUrl),
                    url= CleanDataHelper.deleteMultipleWhiteSpaces(newUrl) ,
                    postDate=str(datetime.datetime.now())
                )
                ScrapingSiteHelper.insertDataToDb(dataJson)
                listArticles.append(dataJson)

    @staticmethod
    def format_url(url, baseUrl):
        if url != None:
            return baseUrl + url
        return ''

    @staticmethod
    def insertDataToDb(data):
        db = DatabaseConfig()
        newsColection = db.getCollection('news')
        newsColection.insert_one(data)
        print('Inserted Correctly')

    @staticmethod
    def saveContentToFile(listArticles, siteName):
        with open(siteName + '.txt', 'wb') as f:
            f.write(str.encode(json.dumps(listArticles), 'utf-8'))