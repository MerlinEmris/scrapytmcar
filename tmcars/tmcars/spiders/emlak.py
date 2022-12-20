import scrapy
import re
from bs4 import BeautifulSoup
from tmcars.items import TmcarsItem


class EmlakSpider(scrapy.Spider):
    name = 'emlak'
    allowed_domains = ['tmcars.info']
    base_url = 'https://tmcars.info'
    start_urls = ['https://tmcars.info/tm/others/emlak?offset=0&max=250&lang=tm']

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')

        # items = response.css("#otherProductTable > div.col-xl-12")
        items = soup.select("#otherProductTable > div.col-xl-12")
        for item in items:

            # relative_url = item.css("div > div
            # > div.col-xl-9.col-lg-8.col-md-8.col-sm-8.col-8.desc-col
            # > div > div > div.item-card2-desc > span > a::attr(href)").get()
            relative_url = item.select(
                "div > div > div.col-xl-9.col-lg-8.col-md-8.col-sm-8.col-8.desc-col"
                " > div > div > div.item-card2-desc > span > a")
            item_url = relative_url[0]['href']
            yield scrapy.Request(item_url, callback=self.parseDetailedItem, meta={'link':item_url})

    def parseDetailedItem(self, response: scrapy.http.Response):

        item_css_selector = 'body > div.content' \
                            ' > section.product-section.product-section.bg-light-v0' \
                            ' > section > div > div > div.col-xl-8.col-lg-8.col-md-12'
        details_css_selector = item_css_selector + ' > div.card.mb-3 > div.card-body.entry-content' \
                                                   ' > div.row.mt-3 > div > div > table > tbody'

        # #slider
        image_css_selector = '#slider'

        selectors = {
            'post_date': item_css_selector + ' > div.card.overflow-hidden'
                                             ' > div > div.item-det.mb-4'
                                             ' > div > ul > li:nth-child(1) > span',
            'views': item_css_selector + ' > div.card.overflow-hidden'
                                         ' > div > div.item-det.mb-4'
                                         ' > div > ul > li:nth-child(3) > span',
            'name':item_css_selector + ' > div.card.overflow-hidden'
                                       ' > div > div.item-det.mb-4 > h1',
            'description': item_css_selector + ' > div.card.mb-3'
                                               ' > div.card-body.entry-content'
                                               ' > div.mb-5.entry-content-text.expanded > p',
        }
        soup = BeautifulSoup(response.text, 'lxml')
        item = TmcarsItem()

        item['link'] = response.meta['link']
        item['post_date'] = soup.select(selectors['post_date'])[0].find(text=True, recursive=False).strip()
        item['views'] = soup.select(selectors['views'])[0].find(text=True, recursive=False).strip()
        item['name'] = soup.select(selectors['name'])[0].find(text=True, recursive=False).strip()
        item['description'] = soup.select(selectors['description'])[0].find(text=True, recursive=False).strip()
        details = {}
        for elem in soup.select(details_css_selector)[0].findAll('td'):
            detail_name = elem.find('span').getText().strip()
            detail_value = elem.find(text=True, recursive=False).strip()
            if detail_name != 'Telefon belgi :':
                details[f'{detail_name[:-2]}'] = detail_value
            else:
                details[f'{detail_name[:-2]}'] = elem.find('a').getText().strip()
        item['details'] = details
        # body > script:nth-child(16)
        selector: str = soup.select('body > script:nth-child(16)')[0].string
        images_selector: str = re.findall(r'images: \[(\S+)]', selector, re.MULTILINE)[0]
        images: list = [image[1:-1] for image in images_selector.split(',')]
        item['images'] = images

        return item
