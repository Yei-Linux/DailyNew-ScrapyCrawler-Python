import json
import datetime
import requests

from DailyNewsSpyder.config.DatabaseConfig import DatabaseConfig
from DailyNewsSpyder.helpers.CleanDataHelper import CleanDataHelper

class ScrapingWikipediaHelper():
    @staticmethod
    def parseDataBySite(response):
        site = response.meta.get('site')
        ScrapingWikipediaHelper.pageNotUsingApi(response,site)

    @staticmethod
    def pageNotUsingApi(response,site):
        topicJson = {}

        for idOfSubtopic in response.css(site['components']['subTitle']):
            try:
                subtitle = response.css("#"+idOfSubtopic.extract()+"::text").get()
                content = response.xpath("//p[preceding-sibling::h2[1][./span[@id = '"+idOfSubtopic.extract()+"']]]//text()").extract()
            except Exception as error:
                print('Caught this error: ' + repr(error))
                continue

            if len(content) > 0:
                if content[0] != '\n':
                    textContent = "".join(content)
                    textContent = CleanDataHelper.deleteIndexWikipedia(textContent)

                    topicJson[idOfSubtopic.extract()] = {
                        "title": subtitle,
                        "content": textContent
                    }

        ScrapingWikipediaHelper.saveContentToFile(topicJson, site['siteName'])

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
    def saveContentToFile(object, siteName):
        with open(siteName + '.txt', 'wb') as f:
            f.write(str.encode(json.dumps(object)))