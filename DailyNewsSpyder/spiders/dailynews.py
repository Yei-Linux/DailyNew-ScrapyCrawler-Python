import scrapy
from scrapy_splash import SplashRequest
import cfscrape
from fake_useragent import UserAgent

from DailyNewsSpyder.constants.scrapingStructure import ScrapingStructure
from DailyNewsSpyder.helpers.ScrapingSiteHelper import ScrapingSiteHelper

class DailyNews(scrapy.Spider):
    name = "dailynews"

    def start_requests(self):
        user_agent = UserAgent().random
        scraperSites = ScrapingStructure.getStructure()

        for site in scraperSites:
            if site['needJs']:
                if site['needIUAM']:
                    token, agent = cfscrape.get_tokens(site['url'], user_agent)
                    yield SplashRequest(url=site['url'],callback=ScrapingSiteHelper.parseDataBySite,args={'lua_source': site["script"]},endpoint='execute',meta={"site": site},cookies=token, headers={'User-Agent': agent})
                else:
                    yield SplashRequest(url=site['url'],callback=ScrapingSiteHelper.parseDataBySite,args={'lua_source': site["script"]},endpoint='execute',meta={"site": site})
            else:
                if site['needIUAM']:
                    token, agent = cfscrape.get_tokens(site['url'], user_agent)
                    yield SplashRequest(url=site['url'],callback=ScrapingSiteHelper.parseDataBySite,meta={"site": site},cookies=token, headers={'User-Agent': agent})
                else:
                    yield SplashRequest(url=site['url'], callback=ScrapingSiteHelper.parseDataBySite, meta={"site": site})

