import json
import datetime
import requests

from DailyNewsSpyder.config.DatabaseConfig import DatabaseConfig
from DailyNewsSpyder.helpers.CleanDataHelper import CleanDataHelper

class ScrapingSiteJobsHelper():
    @staticmethod
    def parseDataBySite(response):
        site = response.meta.get('site')

        if site['hasApi']:
            ScrapingSiteJobsHelper.pageUsingApi(site)
        else:
            ScrapingSiteJobsHelper.pageNotUsingApi(response,site)

    @staticmethod
    def pageUsingApi(site):
        response = requests.get(site['api']['url'],headers=site['api']['headers'])
        print(response.text)

    @staticmethod
    def pageNotUsingApi(response,site):
        for article in response.css(site['components']['article']):
            header = article.css(site['components']['header']).get()
            description = article.css(site['components']['description']).get()
            newUrl = ScrapingSiteJobsHelper.format_url(article.css(site['components']['newUrl']).get(), site['baseUrl'])
            imageUrl = article.css(site['components']['imageUrl']).get()

            if header is not None and description is not None and newUrl is not None and imageUrl is not None:

                if site['imageCurrentValue'] != "" and site['imageValueToReplace'] != "":
                    imageUrl = CleanDataHelper.replaceStrangeCharacteres(imageUrl, site['imageCurrentValue'],site['imageValueToReplace'])

                dataJson = dict(
                    title= CleanDataHelper.deleteMultipleWhiteSpaces(header),
                    description= CleanDataHelper.deleteMultipleWhiteSpaces(description),
                    urlImage= CleanDataHelper.deleteMultipleWhiteSpaces(imageUrl),
                    url= CleanDataHelper.deleteMultipleWhiteSpaces(newUrl),
                    postDate=str(datetime.datetime.now())
                )
                ScrapingSiteJobsHelper.insertDataToDb(dataJson)

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
            f.write(str.encode(listArticles, 'utf-8'))