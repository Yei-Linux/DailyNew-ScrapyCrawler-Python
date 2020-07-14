import scrapy
from scrapy_splash import SplashRequest
import cfscrape
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os

from DailyNewsSpyder.constants.scrapingStructure import ScrapingStructure
from DailyNewsSpyder.helpers.ScrapingWikipediaHelper import ScrapingWikipediaHelper

class WikipediaSpider(scrapy.Spider):
    name = "wikipediaspider"

    def start_requests(self):

        user_agent = UserAgent().random
        scraperSites = ScrapingStructure.getStructureWikipedia()

        for site in scraperSites:
            if site['enabled']:
                if site['needJs']:
                    if site['needIUAM']:
                        token, agent = cfscrape.get_tokens(site['url'], user_agent)
                        yield SplashRequest(url=site['url'],callback=ScrapingWikipediaHelper.parseDataBySite,args={'lua_source': site["script"]},endpoint='execute',meta={"site": site},cookies=token, headers={'User-Agent': agent})
                    else:
                        yield SplashRequest(url=site['url'],callback=ScrapingWikipediaHelper.parseDataBySite,args={'lua_source': site["script"],'customData': site["customData"]},endpoint='execute',meta={"site": site})
                else:
                    if site['needIUAM']:
                        token, agent = cfscrape.get_tokens(site['url'], user_agent)
                        yield SplashRequest(url=site['url'],callback=ScrapingWikipediaHelper.parseDataBySite,meta={"site": site},cookies=token, headers={'User-Agent': agent})
                    else:
                        yield SplashRequest(url=site['url'], callback=ScrapingWikipediaHelper.parseDataBySite, meta={"site": site})

