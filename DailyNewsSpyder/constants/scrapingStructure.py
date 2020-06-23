
class ScrapingStructure():
    @staticmethod
    def getStructure():
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
                            'imageUrl': 'div a div img::attr("src")'
                        },
                        "needJs": False,
                        "needIUAM": False,
                        "script":""
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
                            'imageUrl': 'div.assetThumb a figure img::attr("src")'
                        },
                        "needJs": False,
                        "needIUAM": False,
                        "script": ""
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
                            'imageUrl': 'div.lx-media-asset__image img::attr("src")'
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
                        """
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
                            'imageUrl': 'div.technology-org-summary-picture a img::attr("src")'
                        },
                        "needJs": False,
                        "needIUAM": True,
                        "script": ""
                    }
                ]

