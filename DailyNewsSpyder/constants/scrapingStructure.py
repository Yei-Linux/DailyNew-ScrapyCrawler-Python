
class ScrapingStructure():
    @staticmethod
    def getStructureNews():
      return    [
                    {
                        "siteName": 'theverge',
                        "url": 'https://www.theverge.com/tech',
                        "baseUrl": '',
                        "components": {
                            "article": 'div.c-compact-river__entry',
                            "header": 'div div.c-entry-box--compact__body h2.c-entry-box--compact__title a::text',
                            "description": 'div div.c-entry-box--compact__body h2.c-entry-box--compact__title a::text',
                            "newUrl": 'div div.c-entry-box--compact__body h2.c-entry-box--compact__title a::attr("href")',
                            'imageUrl': 'div a.c-entry-box--compact__image-wrapper div.c-entry-box--compact__image img::attr("src")'
                        },
                        "needJs": False,
                        "needIUAM": False,
                        "script":"",
                        "imageCurrentValue": "",
                        "imageValueToReplace":""
                    },
                    {
                        "siteName": 'cnet',
                        "url": 'https://www.cnet.com/news/',
                        "baseUrl": 'https://www.cnet.com',
                        "components": {
                            "article": 'div.row div.riverPost',
                            "header": 'div.assetText h3 a.assetHed::text',
                            "description": 'div.assetText p a.assetHed::text',
                            "newUrl": 'div.assetText h3 a.assetHed::attr("href")',
                            'imageUrl': 'div.assetThumb a figure img::attr("data-original")'
                        },
                        "needJs": False,
                        "needIUAM": False,
                        "script": "",
                        "imageCurrentValue": "",
                        "imageValueToReplace": ""
                    },
                    {
                        "siteName": 'bbc',
                        "url": 'https://www.bbc.com/news/technology',
                        "baseUrl": 'https://www.bbc.com',
                        "components": {
                            "article": 'article.lx-stream-post',
                            "header": 'h3.lx-stream-post__header-title a.qa-heading-link span.lx-stream-post__header-text::text',
                            "description": 'div.lx-stream-post-body p.qa-sty-summary::text',
                            "newUrl": 'div.lx-stream-post-body a.lx-stream-asset__cta::attr("href")',
                            'imageUrl': 'div.lx-media-asset__image img::attr("data-src")'
                        },
                        "needJs": True,
                        "needIUAM": False,
                        "script": """
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
                        """,
                        "imageCurrentValue": "{width}",
                        "imageValueToReplace": "240"
                    },
                    {
                        "siteName": 'technology-org',
                        "url": 'https://www.technology.org/category/technologies/',
                        "baseUrl": '',
                        "components": {
                            "article": 'div.technology-org-top-category-tag',
                            "header": 'div.technology-org-top-category-tag-content a.technology-org-news-link::text',
                            "description": 'div.technology-org-excerpt::text',
                            "newUrl": 'div.technology-org-top-category-tag-content a.technology-org-news-link::attr("href")',
                            'imageUrl': 'div.technology-org-summary-picture a img::attr("data-src")'
                        },
                        "needJs": False,
                        "needIUAM": True,
                        "script": "",
                        "imageCurrentValue": "",
                        "imageValueToReplace": ""
                    }
                ]

    @staticmethod
    def getStructureJobs():
        return  [
                    {
                        "siteName": 'dice',
                        "url": 'https://www.dice.com/dashboard/login',
                        "baseUrl": 'https://www.dice.com',
                        "components": {
                            "article": '',
                            "header": '',
                            "description": '',
                            "newUrl": '',
                            'imageUrl': ''
                        },
                        "needJs": True,
                        "needIUAM": False,
                        "script": """
                            function main(splash)
                                if splash.args.cookies then
                                    splash:init_cookies(splash.args.cookies)
                                end
                                assert(splash:go{
                                    splash.args.url,
                                    headers=splash.args.headers,
                                    http_method="POST",
                                    formdata=splash.args.customData.credentials
                                })
                                assert(splash:wait(5))
                                
                                local entries = splash:history()
                                local last_response = entries[#entries].response
                                
                                return {
                                    url = splash:url(),
                                    headers = last_response.headers,
                                    http_status = last_response.status,
                                    cookies = splash:get_cookies(),
                                    html = splash:html(),
                                }
                            end
                        """,
                        "hasApi": True,
                        "api":{
                            "url":'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?countryCode2=US&radius=30&radiusUnit=mi&page=1&pageSize=100&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CemployerType%7CeasyApply%7CisRemote&fields=id%7CjobId%7Csummary%7Ctitle%7CpostedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote&culture=en&recommendations=true&interactionId=0&fj=true&includeRemote=true',
                            "headers": {
                                "x-api-key": "1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8"
                            }
                        },
                        "imageCurrentValue": "",
                        "imageValueToReplace": "",
                        "customData":{
                            "credentials": {'email': 'jesusalvan2010@gmail.com', 'password': 'test_scraping_123'}
                        }
                    }
                ]

