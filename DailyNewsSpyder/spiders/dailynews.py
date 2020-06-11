import scrapy
import json
from scrapy_splash import SplashRequest

script="""
function main(splash)
    local url = splash.args.url
    splash:go(url)
    splash:runjs('document.querySelector(".lx-stream-show-more__button").click()')
    splash:wait(1)
    splash:runjs('document.querySelector(".lx-stream-show-more__button").click()')
    splash:wait(1)
    splash:runjs('document.querySelector(".lx-stream-show-more__button").click()')
    splash:wait(1)
    splash:runjs('document.querySelector(".lx-stream-show-more__button").click()')
    splash:wait(1)
    return {
        html = splash:html(),
    }
end
"""

class DailyNews(scrapy.Spider):
    name = "dailynews"

    def start_requests(self):
        print('Entry')
        urls = ['https://www.bbc.com/news/technology']
        for url in urls:
            yield SplashRequest(url=url,callback=self.parse,args={'lua_source': script},endpoint='execute')

    def parse(self,response):
        listArticles = []

        for article in response.css('article.lx-stream-post'):
            header = article.css('h3.lx-stream-post__header-title a.qa-heading-link span.lx-stream-post__header-text::text').get()
            description = article.css('div.lx-stream-post-body p.qa-sty-summary::text').get()
            newUrl = self.format_url(article.css('div.lx-stream-post-body a.lx-stream-asset__cta::attr("href")').get())
            imageUrl = article.css('div.lx-media-asset__image img::attr("src")').get()
            listArticles.append(dict(header=header,description=description,new_url=newUrl,image_url=imageUrl))
        print(listArticles)
        self.saveContentToFile(listArticles)

    def format_url(self,url):
        if url != None:
            return 'https://www.bbc.com' + url
        return ''

    def saveContentToFile(self,listArticles):
        with open('news.txt','wb') as f:
            f.write(str.encode(json.dumps(listArticles),'utf-8'))