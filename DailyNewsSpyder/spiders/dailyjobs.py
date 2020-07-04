import scrapy
from scrapy_splash import SplashRequest
import cfscrape
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os

from DailyNewsSpyder.constants.scrapingStructure import ScrapingStructure
from DailyNewsSpyder.helpers.ScrapingSiteJobsHelper import ScrapingSiteJobsHelper
from DailyNewsSpyder.config.DatabaseConfig import DatabaseConfig

class DailyJobs(scrapy.Spider):
    name = "dailyjobs"

    @staticmethod
    def resetCollectionToStoreNewData():
        load_dotenv()
        db = DatabaseConfig()
        isTruncate = int(os.getenv('IS_TRUNCATE'))
        if isTruncate == 1 :
            db.resetCollection('jobs')

    def start_requests(self):
        DailyJobs.resetCollectionToStoreNewData()

        user_agent = UserAgent().random
        scraperSites = ScrapingStructure.getStructureJobs()

        for site in scraperSites:
            if site['enabled']:
                if site['needJs']:
                    if site['needIUAM']:
                        token, agent = cfscrape.get_tokens(site['url'], user_agent)
                        yield SplashRequest(url=site['url'],callback=ScrapingSiteJobsHelper.parseDataBySite,args={'lua_source': site["script"]},endpoint='execute',meta={"site": site},cookies=token, headers={'User-Agent': agent})
                    else:
                        yield SplashRequest(url=site['url'],callback=ScrapingSiteJobsHelper.parseDataBySite,args={'lua_source': site["script"],'customData': site["customData"]},endpoint='execute',meta={"site": site})
                else:
                    if site['needIUAM']:
                        token, agent = cfscrape.get_tokens(site['url'], user_agent)
                        yield SplashRequest(url=site['url'],callback=ScrapingSiteJobsHelper.parseDataBySite,meta={"site": site},cookies=token, headers={'User-Agent': agent})
                    else:
                        yield SplashRequest(url=site['url'], callback=ScrapingSiteJobsHelper.parseDataBySite, meta={"site": site})

