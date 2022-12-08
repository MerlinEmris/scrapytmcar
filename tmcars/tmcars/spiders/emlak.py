import scrapy
from bs4 import BeautifulSoup
from tmcars.items import TmcarsItem


class EmlakSpider(scrapy.Spider):
    name = 'emlak'
    allowed_domains = ['tmcars.info']
    base_url = 'https://tmcars.info'
    start_urls = ['https://tmcars.info/tm/others/emlak',]

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')

        # items = response.css("#otherProductTable > div.col-xl-12")
        items = soup.select("#otherProductTable > div.col-xl-12")
        for item in items:

            # relative_url = item.css("div > div > div.col-xl-9.col-lg-8.col-md-8.col-sm-8.col-8.desc-col > div > div > div.item-card2-desc > span > a::attr(href)").get()
            relative_url = item.select(
                "div > div > div.col-xl-9.col-lg-8.col-md-8.col-sm-8.col-8.desc-col > div > div > div.item-card2-desc > span > a")
            item_url = relative_url[0]['href']
            yield scrapy.Request(item_url, callback=self.parseDetailedItem, meta={'link':item_url})

    def parseDetailedItem(self, response: scrapy.http.Response):

        item_css_selector = 'body > div.content > section.product-section.product-section.bg-light-v0 > section > div > div > div.col-xl-8.col-lg-8.col-md-12'
        details_css_selector = item_css_selector + ' > div.card.mb-3 > div.card-body.entry-content > div.row.mt-3 > div > div > table > tbody'

        selectors = {
            'post_date': item_css_selector + ' > div.card.overflow-hidden > div > div.item-det.mb-4 > div > ul > li:nth-child(1) > span',
            'views': item_css_selector + ' > div.card.overflow-hidden > div > div.item-det.mb-4 > div > ul > li:nth-child(3) > span',
            'name':item_css_selector + ' > div.card.overflow-hidden > div > div.item-det.mb-4 > h1',
            'description': item_css_selector + ' > div.card.mb-3 > div.card-body.entry-content > div.mb-5.entry-content-text.expanded > p',
        }

        details_name_indicators = [
            ['Ýeri :', 'location'],
            ['Otag sany :', 'room_count'],
            ['Remont :', 'interior_type'],
            ['Telefon belgi :', 'phone'],
            ['Binadaky Gat Sany :','building_floor_count'],
            ['Gat :', 'floor_count'],
            ['Kategoriýa :','category']
        ]

        soup = BeautifulSoup(response.text, 'lxml')
        item = TmcarsItem()

        item['post_date'] = soup.select(selectors['post_date'])[0].find(text=True, recursive=False).strip()
        item['views'] = soup.select(selectors['views'])[0].find(text=True, recursive=False).strip()
        item['name'] = soup.select(selectors['name'])[0].find(text=True, recursive=False).strip()
        item['description'] = soup.select(selectors['description'])[0].find(text=True, recursive=False).strip()
        item['link'] = response.meta['link']
        for elem in soup.select(details_css_selector)[0].findAll('td'):
            detail_name = elem.find('span').getText().strip()
            detail_value = elem.find(text=True, recursive=False).strip()
            for indicator in details_name_indicators:
                if indicator[0] == detail_name:
                    if indicator[1] != 'phone':
                        item[indicator[1]] = detail_value
                    else:
                        item[indicator[1]] = elem.find('a').getText().strip()

        return item
