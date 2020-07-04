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
        responseJson = response.json()
        jobs = responseJson[site['api']['structure']['firstLevel']]

        for job in jobs:
            job = ScrapingSiteJobsHelper.validateJobJson(job,site['api']['structure']['fields'])

            header = job[site['api']['structure']['fields']['header']]
            description = job[site['api']['structure']['fields']['description']]
            imageUrl = job[site['api']['structure']['fields']['imageUrl']]
            newUrl = job[site['api']['structure']['fields']['newUrl']]

            dataJson = dict(
                title=CleanDataHelper.deleteMultipleWhiteSpaces(header),
                description=CleanDataHelper.deleteMultipleWhiteSpaces(description),
                urlImage=CleanDataHelper.deleteMultipleWhiteSpaces(imageUrl),
                url=CleanDataHelper.deleteMultipleWhiteSpaces(newUrl),
                postDate=str(datetime.datetime.now())
            )
            ScrapingSiteJobsHelper.insertDataToDb(dataJson)

    @staticmethod
    def validateJobJson(job,fields):
        if fields['header'] not in job.keys():
            job[fields['header']] = ''
        if fields['description'] not in job.keys():
            job[fields['description']] = ''
        if fields['newUrl'] not in job.keys():
            job[fields['newUrl']] = ''
        if fields['imageUrl'] not in job.keys():
            job[fields['imageUrl']] = ''
        return job

    @staticmethod
    def pageNotUsingApi(response,site):
        for article in response.css(site['components']['article']):
            header = article.css(site['components']['header']).get()
            description = article.css(site['components']['description']).get()
            newUrl = ScrapingSiteJobsHelper.format_url(article.css(site['components']['newUrl']).get(), site['baseUrl'])
            if site['hasImage']:
                imageUrl = article.css(site['components']['imageUrl']).get()
            else:
                imageUrl = ""

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
        newsColection = db.getCollection('jobs')
        newsColection.insert_one(data)
        print('Inserted Correctly')

    @staticmethod
    def saveContentToFile(listArticles, siteName):
        with open(siteName + '.txt', 'wb') as f:
            f.write(str.encode(listArticles, 'utf-8'))