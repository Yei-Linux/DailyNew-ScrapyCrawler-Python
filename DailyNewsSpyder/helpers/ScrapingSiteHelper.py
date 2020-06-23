import json

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
            listArticles.append(dict(header=header, description=description, new_url=newUrl, image_url=imageUrl))

        print(site['siteName'])
        print(listArticles)
        ScrapingSiteHelper.saveContentToFile(listArticles, site['siteName'])

    @staticmethod
    def format_url(url, baseUrl):
        if url != None:
            return baseUrl + url
        return ''

    @staticmethod
    def saveContentToFile(listArticles, siteName):
        with open(siteName + '.txt', 'wb') as f:
            f.write(str.encode(json.dumps(listArticles), 'utf-8'))